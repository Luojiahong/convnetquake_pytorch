def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()
