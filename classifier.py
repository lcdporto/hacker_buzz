import tensorflow as tf
import settings

def temp_hack(results):
    """
    To make it easier for the web client, we are
    goin to return only one option, for that we
    sort the dict and return a new dict with only
    the most probable option, the condition is there
    because in some cases the result is in scientific
    notation and we want to discard those (so we make
    sure the first digit is 0)
    """
    final = {}
    for x in sorted(results, key=results.get, reverse=True):
        if int(results[x][0]) == 0:
            final[x] = results[x]
            break

    return final

def classify(image_path):
    """
    Given a file path return a classification
    """

    results = {}
    
    image_data = tf.gfile.FastGFile(image_path, 'rb').read()

    label_lines = [line.rstrip() for line in tf.gfile.GFile(settings.LABELS)]

    # Unpersists graph from file
    with tf.gfile.FastGFile(settings.GRAPH, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
        predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        
        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            results[human_string] = str(score)

    return temp_hack(results)
