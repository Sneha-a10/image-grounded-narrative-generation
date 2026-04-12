import os
from main_pipeline import run_full_pipeline

def test():

    # Allow both PNG and JPG testing
    image_path = "test.jpg" if os.path.exists("test.jpg") else "test.png"
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Could not find {image_path} in the directory.")
        return

    # 🔴 CHANGE THIS:
    mode = "real"   # or "debug"

    result = run_full_pipeline(image_path, mode=mode)

    print("\n" + "="*50)
    print("🔥 FINAL PIPELINE SUMMARY")
    print("="*50)
    print(f"Decision: {result.get('decision')}")
    print(f"Total Attempts: {result.get('attempts')}")
    
    if "best_score_overall" in result and result["best_score_overall"] > -1.0:
        print(f"\n🏆 BEST SCORE ACROSS ALL RETRIES: {result['best_score_overall']:.4f}")
        print(f"\n📖 BEST GENERATED STORY:\n{result['best_story_overall']}\n")
    elif "final_story" in result:
        print(f"\n🏆 ACCEPTED SCORE: {result.get('final_score', 0):.4f}")
        print(f"\n📖 GENERATED STORY:\n{result['final_story']}\n")
    else:
        print("\n❌ Pipeline failed early, no story returned.")
        print(result)

if __name__ == "__main__":
    test()