#!/usr/bin/env python3
"""
Simple Face Selector for Hedra CLI
Provides ASCII art visualization and numbered selection for multi-face scenarios
"""

import cv2
import numpy as np
import os

class SimpleFaceSelector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.img = cv2.imread(image_path)
        if self.img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        self.original_img = self.img.copy()
        self.faces = []
        
        # Load face detection
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        except Exception as e:
            raise RuntimeError(f"Could not load face detection model: {e}")
    
    def detect_faces(self):
        """Detect faces in the image"""
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        
        # Detect faces with balanced parameters for accuracy
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.15,     # Balanced scale factor
            minNeighbors=6,       # Moderate confidence requirement
            minSize=(40, 40),     # Allow smaller faces but not tiny ones
            maxSize=(400, 400),   # Reasonable maximum size
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # Filter out overlapping detections (non-maximum suppression)
        if len(faces) > 1:
            faces = self._remove_overlapping_faces(faces)
        
        # Sort faces left to right for consistent numbering
        if len(faces) > 1:
            faces = sorted(faces, key=lambda face: face[0])  # Sort by x coordinate
        
        self.faces = faces
        return len(faces)
    
    def _remove_overlapping_faces(self, faces):
        """Remove overlapping face detections using simple non-maximum suppression"""
        if len(faces) <= 1:
            return faces
        
        # Convert to list of [x, y, x2, y2, area] for easier processing
        boxes = []
        for (x, y, w, h) in faces:
            boxes.append([x, y, x + w, y + h, w * h])
        
        # Sort by area (largest first)
        boxes = sorted(boxes, key=lambda x: x[4], reverse=True)
        
        # Keep track of which boxes to keep
        keep = []
        
        for i, box in enumerate(boxes):
            should_keep = True
            
            for kept_box in keep:
                # Calculate intersection over union (IoU)
                x1 = max(box[0], kept_box[0])
                y1 = max(box[1], kept_box[1])
                x2 = min(box[2], kept_box[2])
                y2 = min(box[3], kept_box[3])
                
                if x1 < x2 and y1 < y2:
                    intersection = (x2 - x1) * (y2 - y1)
                    union = box[4] + kept_box[4] - intersection
                    iou = intersection / union if union > 0 else 0
                    
                    # If overlap is too high, don't keep this box
                    if iou > 0.3:  # 30% overlap threshold
                        should_keep = False
                        break
            
            if should_keep:
                keep.append(box)
        
        # Convert back to (x, y, w, h) format
        filtered_faces = []
        for box in keep:
            filtered_faces.append((box[0], box[1], box[2] - box[0], box[3] - box[1]))
        
        return filtered_faces
    
    def create_ascii_layout(self):
        """Create ASCII art representation of face positions"""
        if not len(self.faces):
            return "❌ No faces detected"
        
        # Create a grid representation
        grid_w, grid_h = 24, 8
        grid = [[' ' for _ in range(grid_w)] for _ in range(grid_h)]
        
        img_h, img_w = self.img.shape[:2]
        
        # Map faces to grid positions
        for i, (x, y, w, h) in enumerate(self.faces):
            # Calculate center position
            center_x = x + w/2
            center_y = y + h/2
            
            # Map to grid coordinates
            grid_x = int((center_x / img_w) * (grid_w - 4))  # Leave space for face box
            grid_y = int((center_y / img_h) * (grid_h - 2))
            
            # Calculate face box size on grid
            face_grid_w = max(2, int((w / img_w) * grid_w * 0.3))
            face_grid_h = max(1, int((h / img_h) * grid_h * 0.4))
            
            # Draw face box
            face_num = str(i + 1)
            
            # Draw the face representation
            for dy in range(face_grid_h + 1):
                for dx in range(face_grid_w + 1):
                    y_pos, x_pos = grid_y + dy, grid_x + dx
                    if 0 <= y_pos < grid_h and 0 <= x_pos < grid_w:
                        if dy == 0 or dy == face_grid_h or dx == 0 or dx == face_grid_w:
                            # Border
                            grid[y_pos][x_pos] = '█'
                        elif dy == face_grid_h//2 and dx == face_grid_w//2:
                            # Face number in center
                            grid[y_pos][x_pos] = face_num
                        elif grid[y_pos][x_pos] == ' ':
                            # Fill
                            grid[y_pos][x_pos] = '░'
        
        # Convert grid to string
        ascii_lines = []
        ascii_lines.append("🎭 DETECTED FACES")
        ascii_lines.append("┌" + "─" * grid_w + "┐")
        
        for row in grid:
            ascii_lines.append("│" + "".join(row) + "│")
        
        ascii_lines.append("└" + "─" * grid_w + "┘")
        
        return "\n".join(ascii_lines)
    
    def get_face_descriptions(self):
        """Get simple descriptions and coordinates for each face"""
        descriptions = []
        img_h, img_w = self.img.shape[:2]
        
        for i, (x, y, w, h) in enumerate(self.faces):
            # Calculate normalized center coordinates
            center_x = (x + w/2) / img_w
            center_y = (y + h/2) / img_h
            
            # Simple position description
            if len(self.faces) == 1:
                position = "Center person"
            elif len(self.faces) == 2:
                position = "Left person" if i == 0 else "Right person"
            else:
                # For 3+ people, use left/center/right or numbered
                if i == 0:
                    position = "Leftmost person"
                elif i == len(self.faces) - 1:
                    position = "Rightmost person"
                else:
                    position = f"Person #{i+1}"
            
            descriptions.append({
                'number': i + 1,
                'position': position,
                'coordinates': (center_x, center_y),
                'coord_string': f"({center_x:.3f}, {center_y:.3f})"
            })
        
        return descriptions
    
    def interactive_selection(self):
        """Simple interactive selection interface"""
        num_faces = self.detect_faces()
        
        if num_faces == 0:
            print("❌ No faces detected")
            print("💡 Try: Better lighting, face closer to camera, frontal angle")
            print("🔧 Fallback: Use manual --bounding-box x,y coordinates")
            return None
        
        if num_faces == 1:
            # Auto-select single face
            desc = self.get_face_descriptions()[0]
            print("✅ One face detected - using automatically")
            print(f"📍 Coordinates: {desc['coord_string']}")
            return desc['coordinates']
        
        # Multiple faces - show selection interface
        print(f"🔍 Analyzing faces...")
        print(f"🎭 {num_faces} faces detected\n")
        
        # Show ASCII layout
        print(self.create_ascii_layout())
        print()
        
        # Show numbered options
        descriptions = self.get_face_descriptions()
        for desc in descriptions:
            print(f"[{desc['number']}] {desc['position']:<15} {desc['coord_string']}")
        
        print("[i] Visual selection mode")
        print("[q] Cancel")
        print()
        
        # Get user choice
        while True:
            try:
                choice = input("Choose face (1-{}): ".format(num_faces)).strip().lower()
                
                if choice == 'q' or choice == 'quit':
                    print("Selection cancelled")
                    return None
                
                elif choice == 'i' or choice == 'interactive':
                    return self.visual_selection()
                
                elif choice.isdigit():
                    face_num = int(choice)
                    if 1 <= face_num <= num_faces:
                        selected = descriptions[face_num - 1]
                        print(f"✅ Selected Face {face_num}")
                        print(f"📍 Coordinates: {selected['coord_string']}")
                        return selected['coordinates']
                    else:
                        print(f"❌ Please choose 1-{num_faces}")
                
                else:
                    print("❌ Invalid choice. Please try again.")
                    
            except KeyboardInterrupt:
                print("\nSelection cancelled")
                return None
            except EOFError:
                print("\nSelection cancelled")
                return None
    
    def visual_selection(self):
        """OpenCV visual selection interface"""
        print("🖼️  Opening visual selection...")
        print("   Click on any face to select it")
        print("   Press ENTER to confirm, ESC to cancel")
        
        if not hasattr(cv2, 'namedWindow'):
            print("❌ Visual mode not available (no display)")
            return None
        
        window_name = "Face Selection - Click to Select"
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, self._mouse_callback)
        
        self.selected_face_idx = None
        
        while True:
            display_img = self._draw_faces()
            cv2.imshow(window_name, display_img)
            
            key = cv2.waitKey(30) & 0xFF
            
            if key == ord('\r') or key == ord('\n'):  # Enter
                break
            elif key == 27:  # ESC
                self.selected_face_idx = None
                break
        
        cv2.destroyAllWindows()
        
        if self.selected_face_idx is not None:
            descriptions = self.get_face_descriptions()
            selected = descriptions[self.selected_face_idx]
            print(f"✅ Selected Face {selected['number']}")
            print(f"📍 Coordinates: {selected['coord_string']}")
            return selected['coordinates']
        
        print("No face selected")
        return None
    
    def _mouse_callback(self, event, x, y, flags, param):
        """Handle mouse clicks in visual selection"""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check which face was clicked
            for i, (fx, fy, fw, fh) in enumerate(self.faces):
                if fx <= x <= fx + fw and fy <= y <= fy + fh:
                    self.selected_face_idx = i
                    print(f"Selected Face {i + 1}")
                    return
    
    def _draw_faces(self):
        """Draw face rectangles with numbers for visual selection"""
        img = self.original_img.copy()
        
        for i, (x, y, w, h) in enumerate(self.faces):
            # Color - yellow for normal, green for selected
            color = (0, 255, 0) if self.selected_face_idx == i else (0, 255, 255)
            thickness = 3 if self.selected_face_idx == i else 2
            
            # Draw face rectangle
            cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)
            
            # Face number
            label = f"Face {i + 1}"
            
            # Label background
            label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
            cv2.rectangle(img, (x, y - 35), (x + label_size[0] + 10, y), color, -1)
            
            # Label text
            cv2.putText(img, label, (x + 5, y - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
            
            # Coordinates
            center_x = (x + w/2) / img.shape[1]
            center_y = (y + h/2) / img.shape[0]
            coord_text = f"({center_x:.3f}, {center_y:.3f})"
            cv2.putText(img, coord_text, (x, y + h + 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        # Instructions
        instructions = "Click face to select | ENTER confirm | ESC cancel"
        cv2.putText(img, instructions, (10, img.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        return img
    
    def auto_select_best(self):
        """Auto-select the best face (largest, most centered)"""
        num_faces = self.detect_faces()
        
        if num_faces == 0:
            return None
        
        if num_faces == 1:
            desc = self.get_face_descriptions()[0]
            return desc['coordinates']
        
        # For multiple faces, select the largest one
        largest_idx = 0
        largest_area = 0
        
        for i, (x, y, w, h) in enumerate(self.faces):
            area = w * h
            if area > largest_area:
                largest_area = area
                largest_idx = i
        
        descriptions = self.get_face_descriptions()
        selected = descriptions[largest_idx]
        print(f"🤖 Auto-selected largest face (Face {selected['number']})")
        print(f"📍 Coordinates: {selected['coord_string']}")
        return selected['coordinates']

def select_face(image_path, mode='interactive'):
    """
    Main face selection function
    
    Args:
        image_path: Path to image file
        mode: 'interactive' or 'auto'
    
    Returns:
        Tuple of (x, y) coordinates or None if cancelled
    """
    try:
        selector = SimpleFaceSelector(image_path)
        
        if mode == 'auto':
            return selector.auto_select_best()
        else:
            return selector.interactive_selection()
            
    except ImportError:
        print("❌ OpenCV not available. Install with: pip install opencv-python")
        return None
    except Exception as e:
        print(f"❌ Error in face selection: {e}")
        return None

def preview_faces(image_path):
    """Preview faces without selection"""
    try:
        selector = SimpleFaceSelector(image_path)
        num_faces = selector.detect_faces()
        
        if num_faces == 0:
            print("❌ No faces detected")
            return
        
        print(f"🔍 Detected {num_faces} face(s)")
        print(selector.create_ascii_layout())
        print()
        
        descriptions = selector.get_face_descriptions()
        for desc in descriptions:
            print(f"[{desc['number']}] {desc['position']:<15} {desc['coord_string']}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python face_selector.py <image_path> [mode]")
        print("Modes: interactive (default), auto, preview")
        sys.exit(1)
    
    image_path = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'interactive'
    
    if mode == 'preview':
        preview_faces(image_path)
    else:
        result = select_face(image_path, mode)
        if result:
            print(f"\n🎯 Use: --bounding-box {result[0]:.3f},{result[1]:.3f}")