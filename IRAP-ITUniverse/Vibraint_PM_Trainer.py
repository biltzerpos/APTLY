"""*************************************************************************************
VIBRAINT PREDICTION MODULE TRAINER
THIS PROGRAM TRAINS OUR MODEL WITH THE SAMPLES GENERATED OR SPECIFIED IN THE CSV FILE
IT SAVES THE TRAINED MODEL IN .h5 FORMAT.
OUTPUT OF THIS PROGRAM ARE MODEL, ENCODER AND DECODER h5 FILES WHICH CAN BE LOADED
ANYTIME AND ANYWHERE IN THE PREDICTOR OR ANY OTHER MODULE.
NOTE: FOR RETRAINING THE MODEL WITH UPDATED MODEL PARAMETERS SUCH AS epochs, 
number of LSTM units OR NUMBER OF SAMPLE INPUTS n_samples EITHER GENERATED OR SPECIFIED
IN THE train_file CSV FILE, INDICATED USING generate_seq VARIABLE
************************************************************************************"""

from keras.models import Model
from keras.layers import Input
from keras.layers import LSTM
from keras.layers import Dense
import Vibraint_PM_Initializer as gi
from Vibraint_PM_Initializer import *
import Vibraint_PM_DataGenerator as dg

#call init function from Initializer program


#call the get dataset function from the DataGenerator program
X1, X2, y = dg.get_dataset(n_steps_in, n_steps_out, n_features, n_samples,menu_file,input_file,generate_seq)

# returns train, inference_encoder and inference_decoder models
def define_models(n_input, n_output, n_units):
	# define training encoder
	encoder_inputs = Input(shape=(None, n_input))
	encoder = LSTM(n_units, return_state=True)
	encoder_outputs, state_h, state_c = encoder(encoder_inputs)
	encoder_states = [state_h, state_c]
	# define training decoder
	decoder_inputs = Input(shape=(None, n_output))
	decoder_lstm = LSTM(n_units, return_sequences=True, return_state=True)
	decoder_outputs, _, _ = decoder_lstm(decoder_inputs, initial_state=encoder_states)
	decoder_dense = Dense(n_output, activation=activation)
	decoder_outputs = decoder_dense(decoder_outputs)
	model = Model([encoder_inputs, decoder_inputs], decoder_outputs)
	# define inference encoder
	encoder_model = Model(encoder_inputs, encoder_states)
	# define inference decoder
	decoder_state_input_h = Input(shape=(n_units,))
	decoder_state_input_c = Input(shape=(n_units,))
	decoder_states_inputs = [decoder_state_input_h, decoder_state_input_c]
	decoder_outputs, state_h, state_c = decoder_lstm(decoder_inputs, initial_state=decoder_states_inputs)
	decoder_states = [state_h, state_c]
	decoder_outputs = decoder_dense(decoder_outputs)
	decoder_model = Model([decoder_inputs] + decoder_states_inputs, [decoder_outputs] + decoder_states)
	# return all models
	return model, encoder_model, decoder_model
 
# define the model
train, infenc, infdec = define_models(n_features, n_features, n_units)

# compile the model
train.compile(optimizer=optimizer, loss=loss, metrics=['acc'])

# train model
train.fit([X1, X2], y, epochs=epochs)

#save the models
train.save("model.h5")
infenc.save("encoder.h5")
infdec.save("decoder.h5")
print("Saved model to disk")
