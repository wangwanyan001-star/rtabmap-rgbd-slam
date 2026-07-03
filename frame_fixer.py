import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from tf2_msgs.msg import TFMessage

class FrameFixer(Node):
    def __init__(self):
        super().__init__('frame_fixer')
        self.rgb_sub = self.create_subscription(Image, '/camera/rgb/image_color', self.rgb_cb, 50)
        self.depth_sub = self.create_subscription(Image, '/camera/depth/image', self.depth_cb, 50)
        self.info_sub = self.create_subscription(CameraInfo, '/camera/rgb/camera_info', self.info_cb, 50)
        self.tf_sub = self.create_subscription(TFMessage, '/tf', self.tf_cb, 50)

        self.rgb_pub = self.create_publisher(Image, '/fixed/rgb/image_color', 50)
        self.depth_pub = self.create_publisher(Image, '/fixed/depth/image', 50)
        self.info_pub = self.create_publisher(CameraInfo, '/fixed/rgb/camera_info', 50)
        self.tf_pub = self.create_publisher(TFMessage, '/tf', 50)

    def fix(self, frame_id):
        return frame_id.lstrip('/')

    def rgb_cb(self, msg):
        msg.header.frame_id = self.fix(msg.header.frame_id)
        self.rgb_pub.publish(msg)

    def depth_cb(self, msg):
        msg.header.frame_id = self.fix(msg.header.frame_id)
        self.depth_pub.publish(msg)

    def info_cb(self, msg):
        msg.header.frame_id = self.fix(msg.header.frame_id)
        self.info_pub.publish(msg)

    def tf_cb(self, msg):
        for t in msg.transforms:
            t.header.frame_id = self.fix(t.header.frame_id)
            t.child_frame_id = self.fix(t.child_frame_id)
        self.tf_pub.publish(msg)

def main():
    rclpy.init()
    rclpy.spin(FrameFixer())

if __name__ == '__main__':
    main()
