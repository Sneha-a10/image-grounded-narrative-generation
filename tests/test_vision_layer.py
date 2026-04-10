from vision_layer.encoder import VisionEncoder


def test_image_embedding_shape():
    encoder = VisionEncoder()

    embedding = encoder.encode()

    print("embedding shape:", embedding.shape)

    assert embedding is not None
    assert len(embedding.shape) == 1
    assert embedding.shape[0] == 512