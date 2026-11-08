import cv2
import numpy as np

def apply_tint(img, channel_idx):
    """
    Applies a strict tint by keeping the target channel 
    and clearing the other two channels.
    """
    tinted = img.copy()
    for i in range(3):
        if i != channel_idx:
            tinted[:, :, i] = 0
    return tinted

def adjust_intensity(img, channel_idx, value):
    """
    Adjusts the intensity of a specific channel safely.
    """
    adjusted = img.copy()
    channel_data = adjusted[:, :, channel_idx].astype(np.int16)
    channel_data += value
    adjusted[:, :, channel_idx] = np.clip(channel_data, 0, 255).astype(np.uint8)
    return adjusted

def sanitize_filename(filename):
    """
    Removes invalid characters and spaces using basic string manipulation.
    """
    filename = filename.replace(' ', '_')
    allowed_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    sanitized = ""
    for char in filename:
        if char in allowed_chars:
            sanitized += char
    if not sanitized:
        sanitized = "filtered_output"
    return sanitized + ".png"

def main():
    image_path = 'images.jpeg' 
    original = cv2.imread(image_path)

    if original is None:
        print(f"Error: Could not open or find the image at '{image_path}'.")
        return

    # Track filter states independently
    active_tint = None  
    red_adj = 0
    green_adj = 0
    blue_adj = 0

    print("=" * 50)
    print(" INTERACTIVE IMAGE FILTER CONTROLS ")
    print("=" * 50)
    print(" [r] Apply Red Tint        | [g] Apply Green Tint")
    print(" [b] Apply Blue Tint       | [o] Reset Filters")
    print(" [i] Increase Red (+25)    | [d] Decrease Blue (-25)")
    print(" [↑] Increase Green (+25)  | [↓] Decrease Red (-25)")
    print(" [q] Save and Quit")
    print("=" * 50)

    while True:
        current_image = original.copy()
        
        # 1. Apply active color tint first
        if active_tint == 'r':
            current_image = apply_tint(current_image, 2)
        elif active_tint == 'g':
            current_image = apply_tint(current_image, 1)
        elif active_tint == 'b':
            current_image = apply_tint(current_image, 0)
            
        # 2. Apply stacked intensity modifications
        if red_adj != 0:
            current_image = adjust_intensity(current_image, 2, red_adj)
        if green_adj != 0:
            current_image = adjust_intensity(current_image, 1, green_adj)
        if blue_adj != 0:
            current_image = adjust_intensity(current_image, 0, blue_adj)

        # Show the combined result
        cv2.imshow("Interactive Filters", current_image)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('o'):
            print("→ Reset to Original Image")
            active_tint = None
            red_adj = green_adj = blue_adj = 0
        elif key == ord('r'):
            print("→ Active Tint: Red")
            active_tint = 'r'
        elif key == ord('g'):
            print("→ Active Tint: Green")
            active_tint = 'g'
        elif key == ord('b'):
            print("→ Active Tint: Blue")
            active_tint = 'b'
        elif key == ord('i'):
            print("→ Stacked Red Intensity (+25)")
            red_adj += 25
        elif key == ord('d'):
            print("→ Stacked Blue Intensity (-25)")
            blue_adj -= 25
        elif key == 82 or key == ord('w'):  
            print("→ Stacked Green Intensity (+25)")
            green_adj += 25
        elif key == 84 or key == ord('s'):  
            print("→ Stacked Red Intensity (-25)")
            red_adj -= 25

    # --- Save Processed Image ---
    cv2.destroyAllWindows()
    
    user_filename = input("\nEnter a custom name to save your modified image: ").strip()
    safe_name = sanitize_filename(user_filename)
    
    save_path = "images/" + safe_name
    success = cv2.imwrite(save_path, current_image)
    if success:
        print(f"\n🎉 Success! Your image has been securely saved to: {save_path}")
    else:
        print("\n❌ Error: Failed to save. Check if the 'images/' folder exists.")

# =====================================================================
# CRITICAL TRIGGER LINE: THIS ACCUALLY RUNS THE CODE ABOVE!
# =====================================================================
if __name__ == "__main__":
    main()
