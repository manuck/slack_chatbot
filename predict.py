import tensorflow as tf
import data
import os
import sys
import model as ml

from configs import DEFINES

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


def predict(input):
    # 데이터를 통한 사전 구성 한다.
    char2idx, idx2char, vocabulary_length = data.load_voc()

    # 테스트용 데이터 만드는 부분이다.
    # 인코딩 부분 만든다.

    print(input)
    predic_input_enc = data.enc_processing([input], char2idx)
    # 학습 과정이 아니므로 디코딩 입력은
    # 존재하지 않는다.(구조를 맞추기 위해 넣는다.)
    predic_input_dec = data.dec_input_processing([""], char2idx)
    # 학습 과정이 아니므로 디코딩 출력 부분도
    # 존재하지 않는다.(구조를 맞추기 위해 넣는다.)
    predic_target_dec = data.dec_target_processing([""], char2idx)

    # 에스티메이터 구성한다.
    classifier = tf.estimator.Estimator(
        model_fn=ml.model,  # 모델 등록한다.
        model_dir=DEFINES.check_point_path,  # 체크포인트 위치 등록한다.
        params={  # 모델 쪽으로 파라메터 전달한다.
            'embedding_size': DEFINES.embedding_size,
            'hidden_size': DEFINES.hidden_size,  # 가중치 크기 설정한다.
            'ffn_hidden_size': DEFINES.ffn_hidden_size,
            'attention_head_size': DEFINES.attention_head_size,
            'learning_rate': DEFINES.learning_rate,  # 학습율 설정한다.
            'vocabulary_length': vocabulary_length,  # 딕셔너리 크기를 설정한다.
            'embedding_size': DEFINES.embedding_size,  # 임베딩 크기를 설정한다.
            'layer_size': DEFINES.layer_size,
            'embedding':DEFINES.embedding,
            'max_sequence_length': DEFINES.max_sequence_length,
            'xavier_initializer': DEFINES.xavier_initializer,
            'multilayer': DEFINES.multilayer,
        })

        #TODO

    for i in range(DEFINES.max_sequence_length):
        if i > 0:
            predic_input_dec = data.dec_input_processing([answer], char2idx)
            predic_target_dec = data.dec_target_processing([answer], char2idx)

        # 예측을 하는 부분이다.
        predictions = classifier.predict(input_fn=lambda: data.eval_input_fn(predic_input_enc, predic_input_dec, predic_target_dec, 1))

        answer, finished = data.pred_next_string(predictions, idx2char)

        if finished:
            break
    # 예측한 값을 인지 할 수 있도록
    # 텍스트로 변경하는 부분이다.
    print("answer: ", answer)
    return answer
