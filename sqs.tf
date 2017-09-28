resource "aws_sqs_queue" "pollexy-queue" {
  name                        = "pollexy-queue.fifo"
  fifo_queue                  = true
  content_based_deduplication = true
}

output "sqs_arn" {
    value = "${aws_sqs_queue.pollexy-queue.arn}"
}

output "sqs_id" {
    value = "${aws_sqs_queue.pollexy-queue.id}"
}
