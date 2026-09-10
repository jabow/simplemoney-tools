<?php
/*
 * Contact form handler for simplemoney-tools.co.uk.
 *
 * The site is otherwise fully static; this is the one server-side file.
 * It runs on Hostinger's PHP and delivers to CONTACT_TO via PHP's mail().
 *
 * Deliverability note (important): mail() hands off to the host's local MTA,
 * so the From: address MUST be on this site's own domain for SPF/DMARC to
 * pass at Gmail. The visitor's address goes in Reply-To:, never in From: —
 * putting it in From: is the single most common reason these forms get
 * silently dropped or spam-filed. FROM_ADDRESS does not need a real inbox
 * (nothing replies to it), but the domain's SPF record does need to
 * authorise Hostinger's mail servers. If mail stops arriving, check that
 * first, before anything in this file.
 *
 * Returns JSON so js/main.js can distinguish a real delivery from a
 * failure and show the mailto: fallback rather than claiming success.
 */

declare(strict_types=1);

const CONTACT_TO    = 'SimpleMoneyTools1@gmail.com';
const FROM_ADDRESS  = 'noreply@simplemoney-tools.co.uk';
const FROM_NAME     = 'Simple Money Tools website';

// Light abuse control. This is a low-traffic contact form, not an API —
// a handful of messages per IP per hour is well past normal use.
const RATE_LIMIT_MAX     = 5;
const RATE_LIMIT_WINDOW  = 3600; // seconds

const MAX_NAME    = 120;
const MAX_EMAIL   = 254; // RFC 5321 practical maximum
const MAX_MESSAGE = 5000;

const TOPICS = [
	'general'      => 'General enquiry',
	'tool-support' => 'Tool support',
	'bug-report'   => 'Bug report',
	'feature-request' => 'Feature request',
	'pro-interest' => 'Personal Dashboard Pro',
	'other'        => 'Something else',
];

header('X-Content-Type-Options: nosniff');

/*
 * js/main.js posts with `Accept: application/json` and wants JSON back. A
 * browser with JavaScript off posts the form normally, and would otherwise
 * be shown a page of raw JSON — so that case gets a redirect back to the
 * contact page with the outcome in the query string instead.
 */
// strpos rather than str_contains so this still runs if the host is ever
// set to a PHP 7 branch.
function wantsJson(): bool {
	return strpos($_SERVER['HTTP_ACCEPT'] ?? '', 'application/json') !== false;
}

/** Emit a response and stop. */
function respond(int $status, array $payload): void {
	if (!wantsJson()) {
		$query = ($payload['ok'] ?? false)
			? 'sent=1'
			: 'sent=0&reason=' . rawurlencode((string) ($payload['error'] ?? ''));
		header('Location: contact.html?' . $query . '#contact-form', true, 303);
		exit;
	}

	header('Content-Type: application/json; charset=utf-8');
	http_response_code($status);
	echo json_encode($payload, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
	exit;
}

function fail(string $message, int $status = 400): void {
	respond($status, ['ok' => false, 'error' => $message]);
}

if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
	header('Allow: POST');
	fail('This endpoint only accepts form submissions.', 405);
}

/* ---- Rate limiting ------------------------------------------------------ */

/*
 * Keyed on a hash of the IP rather than the IP itself, so the throttle
 * files don't become an incidental log of who visited the contact page.
 * Best-effort by design: if the temp directory isn't writable, the form
 * still works rather than failing closed on every visitor.
 */
function rateLimitExceeded(): bool {
	$ip = $_SERVER['REMOTE_ADDR'] ?? '';
	if ($ip === '') return false;

	$dir = sys_get_temp_dir() . '/smt-contact';
	if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) return false;

	$file = $dir . '/' . hash('sha256', $ip) . '.json';
	$now  = time();

	$state = ['count' => 0, 'start' => $now];
	if (is_readable($file)) {
		$decoded = json_decode((string) @file_get_contents($file), true);
		if (is_array($decoded) && isset($decoded['count'], $decoded['start'])) {
			// An expired window is treated as no window at all.
			if ($now - (int) $decoded['start'] < RATE_LIMIT_WINDOW) {
				$state = ['count' => (int) $decoded['count'], 'start' => (int) $decoded['start']];
			}
		}
	}

	if ($state['count'] >= RATE_LIMIT_MAX) return true;

	$state['count']++;
	@file_put_contents($file, json_encode($state), LOCK_EX);
	return false;
}

if (rateLimitExceeded()) {
	fail('Too many messages sent from this connection. Please try again later, or email us directly.', 429);
}

/* ---- Input -------------------------------------------------------------- */

function field(string $key): string {
	$raw = $_POST[$key] ?? '';
	if (!is_string($raw)) return '';
	// Strip control characters (including CR/LF) except tab and newline,
	// which are only meaningful in the message body.
	return trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $raw) ?? '');
}

// Honeypot: a field hidden from humans by CSS. Anything that fills it in is
// a bot. Answer with a normal success so it has nothing to tune against.
if (field('website') !== '') {
	respond(200, ['ok' => true]);
}

$name    = field('name');
$email   = field('email');
$topic   = field('topic');
$message = field('message');

if ($name === '' || $email === '' || $topic === '' || $message === '') {
	fail('Please fill in every field.');
}
if (mb_strlen($name) > MAX_NAME || mb_strlen($email) > MAX_EMAIL || mb_strlen($message) > MAX_MESSAGE) {
	fail('That message is longer than this form accepts. Please email us directly instead.');
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
	fail('That email address does not look valid.');
}
// Newlines in a header value would let a submission inject extra headers.
// filter_var above already rejects them in $email; $name is stripped of
// control characters by field(), so both are safe to interpolate below.
if (!array_key_exists($topic, TOPICS)) {
	fail('Please choose a topic from the list.');
}

/* ---- Send --------------------------------------------------------------- */

$topicLabel = TOPICS[$topic];
$subject    = sprintf('[Simple Money Tools] %s — %s', $topicLabel, $name);

$body = implode("\n", [
	'New message from the simplemoney-tools.co.uk contact form.',
	'',
	'Name:    ' . $name,
	'Email:   ' . $email,
	'Topic:   ' . $topicLabel,
	'Sent:    ' . gmdate('Y-m-d H:i:s') . ' UTC',
	'',
	str_repeat('-', 60),
	'',
	$message,
	'',
]);

// mb_encode_mimeheader keeps non-ASCII names and subjects legible instead
// of arriving as mojibake.
mb_internal_encoding('UTF-8');
$encodedSubject = mb_encode_mimeheader($subject, 'UTF-8', 'B');
$encodedFrom    = mb_encode_mimeheader(FROM_NAME, 'UTF-8', 'B');

$headers = [
	'MIME-Version: 1.0',
	'Content-Type: text/plain; charset=UTF-8',
	'Content-Transfer-Encoding: 8bit',
	sprintf('From: %s <%s>', $encodedFrom, FROM_ADDRESS),
	sprintf('Reply-To: %s', $email),
	'X-Mailer: simplemoney-tools-contact',
];

// The -f flag sets the envelope sender, which is what SPF is actually
// checked against — without it the host's default is used and alignment
// with the From: domain above is not guaranteed.
$sent = @mail(
	CONTACT_TO,
	$encodedSubject,
	$body,
	implode("\r\n", $headers),
	'-f' . FROM_ADDRESS
);

if (!$sent) {
	fail('The message could not be sent just now. Please email us directly instead.', 502);
}

respond(200, ['ok' => true]);
