from vision_layer.captioner import ImageCaptioner


def test_caption_generation():
    captioner = ImageCaptioner()

    caption = captioner.generate_caption("test.png")

    print("caption:", caption)

    assert caption is not None
    assert isinstance(caption, str)
    assert len(caption) > 0