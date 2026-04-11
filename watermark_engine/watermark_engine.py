import numpy as np
import cv2

def embed_id(frame, distributor_id):
    binary = format(distributor_id, '032b')
    flat = frame.flatten().astype(np.int32)
    for i, bit in enumerate(binary):
        flat[i] = (flat[i] & 0xFE) | int(bit)
    return flat.reshape(frame.shape).astype(np.uint8)

def extract_id(frame):
    flat = frame.flatten()
    bits = ''.join([str(flat[i] & 1) for i in range(32)])
    return int(bits, 2)

def embed_watermark_video(input_path, output_path, distributor_id):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        marked_frame = embed_id(frame, distributor_id)
        out.write(marked_frame)
        frame_count += 1
    cap.release()
    out.release()
    print(f"Done. {frame_count} frames watermarked")

def extract_watermark_video(video_path):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        return None
    return extract_id(frame)

if __name__ == "__main__":
    frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
    test_ids = [1, 7, 42, 999, 65535]
    print("Running SentinelMark watermark engine tests...\n")
    all_passed = True
    for test_id in test_ids:
        marked = embed_id(frame.copy(), test_id)
        recovered = extract_id(marked)
        status = "PASS" if recovered == test_id else "FAIL"
        if status == "FAIL":
            all_passed = False
        print(f"  [{status}] Embedded: {test_id:<6} | Extracted: {recovered}")
    print()
    if all_passed:
        print("ALL TESTS PASSED — SentinelMark engine ready.")
    else:
        print("SOME TESTS FAILED.")