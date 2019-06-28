#!/usr/bin/env python3
import json
import os
import numpy as np
import tensorflow as tf

from modules.model import default_hparams
from modules.sample import sample_sequence
from modules.encoder import Encoder, get_encoder


class State:
    '''
    A wrapper for tf related data, to simplify persistence
    '''
    def __init__(self, session: tf.Session, output,
                 encoder: Encoder, context):
        self.session: tf.Session = session
        self.output = output
        self.encoder: Encoder = encoder
        self.context = context

    def close_session(self):
        self.session.close()


def predict(state: State, input_text):
    context_tokens = state.encoder.encode(input_text)
    out = state.session.run(state.output, feed_dict={
        state.context: [context_tokens]
    })[:, len(context_tokens):]
    text = state.encoder.decode(out[0])
    return text


def interact_model(
    seed=None,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=0
) -> State:
    """
    Interactively run the model
    :seed=None : Integer seed for random number generators,
        fix seed to reproduce results
    :batch_size=1 : Number of batches (only affects speed/memory).
        Must divide nsamples.
    :length=None : Number of tokens in generated text, if None (default), is
        determined by model hyperparameters
    :temperature=1 : Float value controlling randomness in boltzmann
        distribution. Lower temperature results in less random completions.
        As the temperature approaches zero, the model will become deterministic
        and repetitive. Higher temperature results in more random completions.
    :top_k=0 : Integer value controlling diversity. 1 means only 1 word is
        considered for each step (token), resulting in deterministic
        completions, while 40 means 40 words are considered at each step.
        0 (default) is a special setting meaning no restrictions.
        40 generally is a good value.
    """
    if batch_size is None:
        batch_size = 1

    enc = get_encoder()
    hparams = default_hparams()
    with open(os.path.join('/tmp/hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError(
            "Can't get samples longer than window size: %s" % hparams.n_ctx)

    sess = tf.Session()
    context = tf.placeholder(tf.int32, [batch_size, None])
    np.random.seed(seed)
    tf.set_random_seed(seed)
    output = sample_sequence(
        hparams=hparams, length=length,
        context=context,
        batch_size=batch_size,
        temperature=temperature, top_k=top_k
    )

    saver = tf.train.Saver()
    ckpt = tf.train.latest_checkpoint('/tmp')
    saver.restore(sess, ckpt)

    return State(
        session=sess,
        output=output,
        encoder=enc,
        context=context
    )
