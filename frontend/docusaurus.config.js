module.exports = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Learn ROS 2, Simulation, NVIDIA Isaac & VLA',
  url: 'https://your-username.github.io',
  baseUrl: '/hackathon-I/',
  organizationName: 'your-username',
  projectName: 'hackathon-I',

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
