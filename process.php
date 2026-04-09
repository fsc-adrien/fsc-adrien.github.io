<?php
// Security & Error Handling
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', dirname(__FILE__) . '/logs/php-errors.log');

// Only allow POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    exit(json_encode(['success' => false, 'message' => 'Method not allowed']));
}

// Rate limiting - prevent spam
$ip = $_SERVER['REMOTE_ADDR'];
$rate_limit_file = dirname(__FILE__) . '/logs/rate_limit_' . md5($ip) . '.txt';

// Create logs directory if not exists
if (!is_dir(dirname(__FILE__) . '/logs')) {
    mkdir(dirname(__FILE__) . '/logs', 0700, true);
}

if (file_exists($rate_limit_file)) {
    $last_request = (int)file_get_contents($rate_limit_file);
    if (time() - $last_request < 300) { // 5 minutes cooldown
        http_response_code(429);
        exit(json_encode(['success' => false, 'message' => 'Too many requests. Please try again later.']));
    }
}
file_put_contents($rate_limit_file, time());

// Validate and sanitize input
$name = sanitize_input($_POST['name'] ?? '');
$email = sanitize_email($_POST['email'] ?? '');
$subject = sanitize_input($_POST['subject'] ?? '');
$message = sanitize_input($_POST['message'] ?? '');

// Validate required fields
$errors = [];
if (empty($name)) $errors[] = 'Name is required';
if (empty($email)) $errors[] = 'Email is required';
if (empty($subject)) $errors[] = 'Subject is required';
if (empty($message)) $errors[] = 'Message is required';

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    $errors[] = 'Invalid email format';
}

if (strlen($message) < 10 || strlen($message) > 5000) {
    $errors[] = 'Message must be between 10 and 5000 characters';
}

if (!empty($errors)) {
    http_response_code(400);
    exit(json_encode(['success' => false, 'errors' => $errors]));
}

// Build email
$to = "sales@fsc-software.com";
$headers = "From: noreply@fsc-software.com\r\n";
$headers .= "Reply-To: " . $email . "\r\n";
$headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

$body = "New Contact Form Submission\n";
$body .= "============================\n\n";
$body .= sprintf("%-20s: %s\n", "Name", $name);
$body .= sprintf("%-20s: %s\n", "Email", $email);
$body .= sprintf("%-20s: %s\n", "Subject", $subject);
$body .= sprintf("%-20s: %s\n", "IP Address", $ip);
$body .= sprintf("%-20s: %s\n", "Date", date('Y-m-d H:i:s'));
$body .= "\nMessage:\n";
$body .= str_repeat("-", 50) . "\n";
$body .= $message . "\n";

// Send email
if (@mail($to, "[FSC Contact] " . $subject, $body, $headers)) {
    http_response_code(200);
    echo json_encode(['success' => true, 'message' => 'Thank you! Your message has been sent successfully.']);
} else {
    http_response_code(500);
    exit(json_encode(['success' => false, 'message' => 'Failed to send message. Please try again later.']));
}

// Security functions
function sanitize_input($input) {
    $input = trim($input);
    $input = stripslashes($input);
    $input = htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
    return $input;
}

function sanitize_email($email) {
    $email = trim($email);
    $email = filter_var($email, FILTER_SANITIZE_EMAIL);
    return $email;
}
?>