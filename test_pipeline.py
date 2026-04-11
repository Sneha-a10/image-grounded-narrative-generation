from main_pipeline import run_full_pipeline

def test():

    image_path = "test.png"

    # 🔴 CHANGE THIS:
    mode = "real"   # or "real"

    result = run_full_pipeline(image_path, mode=mode)

    print("\n🔥 OUTPUT:")
    print(result)


if __name__ == "__main__":
    test()