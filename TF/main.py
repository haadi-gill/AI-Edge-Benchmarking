from ai_edge_litert.interpreter import Interpreter

# feature contains input_ids, input_mask and segment_ids, which are all
# retrieved from input preprocessing, and are tensors of shape
# [batch_size, max_seq_length], where max_seq_length = 384.

# Load TFLite model and allocate tensors.
tflite_file = '1.tflite'
interpreter = Interpreter(model_path=tflite_file)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test model on random input data.
input_ids = feature["input_ids"]
input_mask = feature["input_mask"]
segment_ids = feature["segment_ids"]

input_ids = np.array(input_ids, dtype=np.int32)
input_mask = np.array(input_mask, dtype=np.int32)
segment_ids = np.array(segment_ids, dtype=np.int32)

interpreter.set_tensor(input_details[0]["index"], input_ids)
interpreter.set_tensor(input_details[1]["index"], input_mask)
interpreter.set_tensor(input_details[2]["index"], segment_ids)
interpreter.invoke()

# Get output logits.
end_logits = interpreter.get_tensor(output_details[0]["index"])[0]
start_logits = interpreter.get_tensor(output_details[1]["index"])[0]

print(start_logits)
print(end_logits)
