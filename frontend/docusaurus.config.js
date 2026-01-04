// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'Learn ROS 2, Simulation, NVIDIA Isaac & VLA',
  url: 'https://physical-ai-and-humanoid-robotic.vercel.app',
  baseUrl: '/',
  organizationName: 'MAHNOORSHK',
  projectName: 'Physical-AI-and-Humanoid-Robotic',

  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

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
        {
          href: 'https://github.com/MAHNOORSHK/Physical-AI-and-Humanoid-Robotic',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      copyright: `Physical AI & Humanoid Robotics Course. Built with Docusaurus.`,
    },
    prism: {
      theme: require('prism-react-renderer').themes.github,
      darkTheme: require('prism-react-renderer').themes.dracula,
      additionalLanguages: ['python', 'bash', 'yaml'],
    },
  },
};

module.exports = config;
