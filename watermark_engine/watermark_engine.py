# import numpy as np
# import cv2

# def embed_id(frame, distributor_id):
#     binary = format(distributor_id, '032b')
#     flat = frame.flatten().astype(np.int32)
#     for i, bit in enumerate(binary):
#         flat[i] = (flat[i] & 0xFE) | int(bit)
#     return flat.reshape(frame.shape).astype(np.uint8)

# def extract_id(frame):
#     flat = frame.flatten()
#     bits = ''.join([str(flat[i] & 1) for i in range(32)])
#     return int(bits, 2)

# def embed_watermark_video(input_path, output_path, distributor_id):
#     cap = cv2.VideoCapture(input_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
#     frame_count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         marked_frame = embed_id(frame, distributor_id)
#         out.write(marked_frame)
#         frame_count += 1
#     cap.release()
#     out.release()
#     print(f"Done. {frame_count} frames watermarked")

# def extract_watermark_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     ret, frame = cap.read()
#     cap.release()
#     if not ret:
#         return None
#     return extract_id(frame)

# if __name__ == "__main__":

#     # Test 1 - frame level
#     frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
#     marked = embed_id(frame.copy(), 42)
#     recovered = extract_id(marked)
#     print(f"Frame test: Embedded 42 | Extracted {recovered}")

#     # Create test video using Python directly
#     print("\nCreating test video...")
#     test_input = "test_video.mp4"
#     test_output = "test_video_watermarked.mp4"

#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     writer = cv2.VideoWriter(test_input, fourcc, 10.0, (640, 480))
    
#     for i in range(30):
#         color_frame = np.zeros((480, 640, 3), dtype=np.uint8)
#         color_frame[:] = (i * 8, 100, 200)
#         writer.write(color_frame)
    
#     writer.release()
#     print(f"Test video created successfully")

#     # Watermark it
#     distributor_id = 7
#     print(f"\nWatermarking with distributor ID: {distributor_id}")
#     embed_watermark_video(test_input, test_output, distributor_id)

#     # Read it back
#     print(f"\nReading watermark from output video...")
#     extracted = extract_watermark_video(test_output)
#     print(f"Extracted distributor ID: {extracted}")

#     if extracted == distributor_id:
#         print("\nSUCCESS — video watermarking works end to end.")
#     else:
#         print(f"\nFAILED — expected {distributor_id}, got {extracted}")


# import numpy as np
# import cv2

# # SentinelMark Watermark Engine
# # Uses redundant LSB embedding — each bit stored in 100 pixels
# # Majority voting on extraction survives mild video compression

# PIXELS_PER_BIT = 200  # each bit embedded 100 times for redundancy

# def embed_id(frame, distributor_id):
#     binary = format(distributor_id, '032b')
#     flat = frame.flatten().astype(np.int32)
#     for bit_idx, bit in enumerate(binary):
#         for j in range(PIXELS_PER_BIT):
#             pixel_idx = bit_idx * PIXELS_PER_BIT + j
#             if pixel_idx < len(flat):
#                 flat[pixel_idx] = (flat[pixel_idx] & 0xFE) | int(bit)
#     return flat.reshape(frame.shape).astype(np.uint8)


# def extract_id(frame):
#     flat = frame.flatten()
#     bits = []
#     for bit_idx in range(32):
#         votes = []
#         for j in range(PIXELS_PER_BIT):
#             pixel_idx = bit_idx * PIXELS_PER_BIT + j
#             if pixel_idx < len(flat):
#                 votes.append(flat[pixel_idx] & 1)
#         # Majority vote — if more than half say 1, bit is 1
#         bit = 1 if sum(votes) > len(votes) / 2 else 0
#         bits.append(str(bit))
#     return int(''.join(bits), 2)


# def embed_watermark_video(input_path, output_path, distributor_id):
#     cap = cv2.VideoCapture(input_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
#     frame_count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         marked_frame = embed_id(frame, distributor_id)
#         out.write(marked_frame)
#         frame_count += 1
#     cap.release()
#     out.release()
#     print(f"Done. {frame_count} frames watermarked")


# def extract_watermark_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     ret, frame = cap.read()
#     cap.release()
#     if not ret:
#         return None
#     return extract_id(frame)


# if __name__ == "__main__":

#     # Test 1 - frame level (no compression)
#     print("Test 1 — Frame level (no compression)")
#     frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
#     for test_id in [1, 7, 42, 999]:
#         marked = embed_id(frame.copy(), test_id)
#         recovered = extract_id(marked)
#         status = "PASS" if recovered == test_id else "FAIL"
#         print(f"  [{status}] Embedded: {test_id} | Extracted: {recovered}")

#     # Test 2 - full video with compression
#     print("\nTest 2 — Full video with mp4v compression")
#     test_input = "test_video.mp4"
#     test_output = "test_video_watermarked.mp4"

#     # Create test video
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     writer = cv2.VideoWriter(test_input, fourcc, 10.0, (640, 480))
#     for i in range(30):
#         color_frame = np.zeros((480, 640, 3), dtype=np.uint8)
#         color_frame[:] = (i * 8, 100, 200)
#         writer.write(color_frame)
#     writer.release()
#     print("  Test video created (30 frames)")

#     # Watermark and extract
#     distributor_id = 7
#     embed_watermark_video(test_input, test_output, distributor_id)
#     extracted = extract_watermark_video(test_output)
#     print(f"  Embedded: {distributor_id} | Extracted: {extracted}")

#     if extracted == distributor_id:
#         print("\nSUCCESS — video watermarking survives compression.")
#     else:
#         print(f"\nFAILED — expected {distributor_id}, got {extracted}")
#         print("Tip: try reducing PIXELS_PER_BIT to 50 or increasing to 200")

# import numpy as np
# import cv2

# # SentinelMark Watermark Engine v3
# # Uses AVI format (less compression) + stronger bit embedding
# # Embeds each bit by forcing pixel values strongly odd or even

# PIXELS_PER_BIT = 150

# def embed_id(frame, distributor_id):
#     binary = format(distributor_id, '032b')
#     flat = frame.flatten().astype(np.int32)
#     for bit_idx, bit in enumerate(binary):
#         for j in range(PIXELS_PER_BIT):
#             pixel_idx = bit_idx * PIXELS_PER_BIT + j
#             if pixel_idx < len(flat):
#                 if int(bit) == 1:
#                     # Force pixel strongly ODD (e.g. 255, 251, 247...)
#                     flat[pixel_idx] = max(1, (flat[pixel_idx] | 1))
#                 else:
#                     # Force pixel strongly EVEN (e.g. 0, 4, 8...)
#                     flat[pixel_idx] = (flat[pixel_idx] & 0xFE)
#     return flat.reshape(frame.shape).astype(np.uint8)


# def extract_id(frame):
#     flat = frame.flatten()
#     bits = []
#     for bit_idx in range(32):
#         votes = []
#         for j in range(PIXELS_PER_BIT):
#             pixel_idx = bit_idx * PIXELS_PER_BIT + j
#             if pixel_idx < len(flat):
#                 votes.append(int(flat[pixel_idx]) & 1)
#         bit = 1 if sum(votes) > len(votes) / 2 else 0
#         bits.append(str(bit))
#     return int(''.join(bits), 2)


# def embed_watermark_video(input_path, output_path, distributor_id):
#     cap = cv2.VideoCapture(input_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#     # Use XVID codec with AVI — much less lossy than mp4v
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

#     frame_count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         marked_frame = embed_id(frame, distributor_id)
#         out.write(marked_frame)
#         frame_count += 1

#     cap.release()
#     out.release()
#     print(f"Done. {frame_count} frames watermarked → {output_path}")


# def extract_watermark_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     ret, frame = cap.read()
#     cap.release()
#     if not ret:
#         return None
#     return extract_id(frame)


# if __name__ == "__main__":

#     # Test 1 - frame level
#     print("Test 1 — Frame level (no compression)")
#     frame = np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8)
#     all_pass = True
#     for test_id in [1, 7, 42, 999, 12345]:
#         marked = embed_id(frame.copy(), test_id)
#         recovered = extract_id(marked)
#         status = "PASS" if recovered == test_id else "FAIL"
#         if status == "FAIL":
#             all_pass = False
#         print(f"  [{status}] Embedded: {test_id:<6} | Extracted: {recovered}")

#     # Test 2 - full video with AVI format
#     print("\nTest 2 — Full video (AVI/XVID format)")
#     test_input  = "test_input.avi"
#     test_output = "test_watermarked.avi"

#     # Create test video as AVI
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     writer = cv2.VideoWriter(test_input, fourcc, 10.0, (640, 480))
#     for i in range(30):
#         color_frame = np.zeros((480, 640, 3), dtype=np.uint8)
#         color_frame[:] = (i * 8, 100, 200)
#         writer.write(color_frame)
#     writer.release()
#     print("  Test video created (30 frames, AVI format)")

#     # Watermark
#     distributor_id = 7
#     print(f"  Embedding distributor ID: {distributor_id}")
#     embed_watermark_video(test_input, test_output, distributor_id)

#     # Extract
#     extracted = extract_watermark_video(test_output)
#     print(f"  Embedded: {distributor_id} | Extracted: {extracted}")

#     if extracted == distributor_id:
#         print("\nSUCCESS — watermark survives video compression!")
#         print("SentinelMark engine is production ready.")
#     else:
#         print(f"\nFAILED — expected {distributor_id}, got {extracted}")


# import numpy as np
# import cv2

# PIXELS_PER_BIT = 150

# def embed_id(frame, distributor_id):
#     binary = format(distributor_id, '032b')
#     flat = frame.flatten().astype(np.int32)
#     for bit_idx, bit in enumerate(binary):
#         for j in range(PIXELS_PER_BIT):
#             idx = bit_idx * PIXELS_PER_BIT + j
#             if idx < len(flat):
#                 if int(bit) == 1:
#                     flat[idx] = max(1, (flat[idx] | 1))
#                 else:
#                     flat[idx] = (flat[idx] & 0xFE)
#     return flat.reshape(frame.shape).astype(np.uint8)

# def extract_id(frame):
#     flat = frame.flatten()
#     bits = []
#     for bit_idx in range(32):
#         votes = []
#         for j in range(PIXELS_PER_BIT):
#             idx = bit_idx * PIXELS_PER_BIT + j
#             if idx < len(flat):
#                 votes.append(int(flat[idx]) & 1)
#         bits.append('1' if sum(votes) > len(votes)/2 else '0')
#     return int(''.join(bits), 2)

# def embed_watermark_video(input_path, output_path, distributor_id):
#     cap = cv2.VideoCapture(input_path)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))
#     count = 0
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break
#         out.write(embed_id(frame, distributor_id))
#         count += 1
#     cap.release()
#     out.release()
#     print(f"Done. {count} frames watermarked -> {output_path}")
#     return count

# def extract_watermark_video(video_path):
#     cap = cv2.VideoCapture(video_path)
#     ret, frame = cap.read()
#     cap.release()
#     if not ret:
#         return None
#     return extract_id(frame)

# if __name__ == "__main__":
#     # Create AVI test video using Python
#     fourcc = cv2.VideoWriter_fourcc(*'XVID')
#     writer = cv2.VideoWriter('test.avi', fourcc, 10.0, (640, 480))
#     for i in range(30):
#         f = np.zeros((480, 640, 3), dtype=np.uint8)
#         f[:] = (i * 8, 100, 200)
#         writer.write(f)
#     writer.release()
#     print("Test video created")

#     # Watermark it
#     embed_watermark_video('test.avi', 'test_watermarked.avi', 7)

#     # Extract and verify
#     result = extract_watermark_video('test_watermarked.avi')
#     print(f"Embedded: 7 | Extracted: {result}")
#     if result == 7:
#         print("SUCCESS - video watermarking works!")
#     else:
#         print(f"FAILED - got {result}")

import numpy as np
import cv2

PIXELS_PER_BIT = 1000  # Robust watermarking

# ===============================
# Embed ID into frame
# ===============================
def embed_id(frame, distributor_id):
    binary = format(distributor_id, '032b')
    flat = frame.flatten().astype(np.int32)

    for bit_idx, bit in enumerate(binary):
        for j in range(PIXELS_PER_BIT):
            idx = bit_idx * PIXELS_PER_BIT + j
            if idx < len(flat):
                if int(bit) == 1:
                    flat[idx] = max(1, (flat[idx] | 1))
                else:
                    flat[idx] = (flat[idx] & 0xFE)

    return flat.reshape(frame.shape).astype(np.uint8)


# ===============================
# Extract ID from frame
# ===============================
def extract_id(frame):
    flat = frame.flatten()
    bits = []

    for bit_idx in range(32):
        votes = []
        for j in range(PIXELS_PER_BIT):
            idx = bit_idx * PIXELS_PER_BIT + j
            if idx < len(flat):
                votes.append(int(flat[idx]) & 1)

        bits.append('1' if sum(votes) > len(votes) / 2 else '0')

    return int(''.join(bits), 2)


# ===============================
# Embed watermark into video
# ===============================
def embed_watermark_video(input_path, output_path, distributor_id):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print("❌ Error opening input video")
        return 0

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or fps is None:
        fps = 30

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if w == 0 or h == 0:
        print("❌ Invalid video dimensions")
        return 0

    # 🔥 LOSSLESS codec (critical for accuracy)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

    if not out.isOpened():
        print("❌ VideoWriter failed")
        return 0

    count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame is None:
            continue

        watermarked = embed_id(frame, distributor_id)
        out.write(watermarked)
        count += 1

    cap.release()
    out.release()

    print(f"✅ Done. {count} frames watermarked → {output_path}")
    return count


# ===============================
# Extract watermark from video
# ===============================
def extract_watermark_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("❌ Error opening video")
        return None

    ret, frame = cap.read()
    cap.release()

    if not ret or frame is None:
        return None

    return extract_id(frame)


# ===============================
# TEST RUN
# ===============================
if __name__ == "__main__":

    # ✅ Create test video (LOSSLESS)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    writer = cv2.VideoWriter('test.avi', fourcc, 10.0, (640, 480))

    for i in range(30):
        f = np.zeros((480, 640, 3), dtype=np.uint8)
        f[:] = (i * 8, 100, 200)
        writer.write(f)

    writer.release()
    print("🎥 Test video created")

    # ✅ Watermark embed
    embed_watermark_video('test.avi', 'test_watermarked.avi', 7)

    # ✅ Extract watermark
    result = extract_watermark_video('test_watermarked.avi')

    print(f"Embedded: 7 | Extracted: {result}")

    if result == 7:
        print("✅ SUCCESS - video watermarking works!")
    else:
        print(f"❌ FAILED - got {result}")