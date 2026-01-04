module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Learn ROS 2, Simulation, NVIDIA Isaac & VLA',
  url: 'https://physical-ai-and-humanoid-robotic.vercel.app',
  baseUrl: '/',
  organizationName: 'MAHNOORSHK',
  projectName: 'Physical-AI-and-Humanoid-Robotic',

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: '/',
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],

  themeConfig: {
    navbar: {
      title: 'Physical AI',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Course',
        },
      ],
    },
  },
};
