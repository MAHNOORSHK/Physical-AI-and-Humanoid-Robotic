module.exports = {
  tutorialSidebar: [
    {
      type: 'doc',
      id: 'intro',
      label: '🏠 Welcome',
    },

    {
      type: 'category',
      label: '🤖 Module 1: ROS 2',
      collapsed: false,
      items: [
        'module-01-ros2/chapter-01-ros2-architecture',
        'module-01-ros2/chapter-02-topics-services-actions',
        'module-01-ros2/chapter-03-building-with-rclpy',
      ],
    },

    {
      type: 'category',
      label: '🎮 Module 2: Simulation',
      collapsed: true,
      items: [
        'module-02-simulation/intro',
        'module-02-simulation/chapter-04-gazebo-physics',
      ],
    },

    {
      type: 'category',
      label: '🧠 Module 3: NVIDIA Isaac',
      collapsed: true,
      items: [
        'module-03-isaac/intro',
        'module-03-isaac/chapter-07-isaac-sim',
      ],
    },

    {
      type: 'category',
      label: '👁️ Module 4: VLA',
      collapsed: true,
      items: [
        'module-04-vla/intro',
        'module-04-vla/chapter-11-voice-to-action',
      ],
    },

    {
      type: 'category',
      label: '📚 Resources',
      collapsed: true,
      items: [
        'hardware-requirements',
        'lab-setup',
      ],
    },
  ],
};
