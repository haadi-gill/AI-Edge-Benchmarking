from ai_edge_litert.interpreter import Interpreter
import numpy as np
import time
# feature contains input_ids, input_mask and segment_ids, which are all
# retrieved from input preprocessing, and are tensors of shape
# [batch_size, max_seq_length], where max_seq_length = 384.

# Load TFLite model and allocate tensors.


tflite_file = './1.tflite'
interpreter = Interpreter(model_path=tflite_file)
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test the model on random input data.
input_shape = input_details[0]['shape']
input_data = np.array(np.random.random_sample(input_shape), dtype=np.int32)
interpreter.set_tensor(input_details[0]['index'], input_data)
start_time = time.time()
interpreter.invoke()
end_time = time.time()
# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
output_data = interpreter.get_tensor(output_details[0]['index'])
#print(output data)
print("elapsed time", end_time - start_time, "seconds")


