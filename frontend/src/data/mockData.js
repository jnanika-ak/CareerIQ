export const mockUserData = {
  name: 'Alex Morgan',
  title: 'Aspiring Data Analyst',
  avatar: 'AM',
  targetRole: 'Data Analyst / BI Specialist',
  status: 'Actively Preparing',
}

export const mockStatCards = [
  {
    id: 'readiness',
    title: 'Job Readiness Score',
    value: '78%',
    change: '+4% from last week',
    isPositive: true,
    tag: 'Demo Metric',
    icon: 'target',
  },
  {
    id: 'matched-skills',
    title: 'Skills Matched',
    value: '8',
    subtext: 'Out of 12 required competencies',
    isPositive: true,
    tag: 'Profile Analysis',
    icon: 'checkCircle',
  },
  {
    id: 'recommended-jobs',
    title: 'Recommended Jobs',
    value: '12',
    subtext: 'High compatibility matches',
    isPositive: true,
    tag: 'Market Intelligence',
    icon: 'briefcase',
  },
  {
    id: 'skill-gaps',
    title: 'Skill Gaps',
    value: '4',
    subtext: 'Priority areas to bridge',
    isPositive: false,
    tag: 'Growth Areas',
    icon: 'alertTriangle',
  },
]

export const mockReadinessData = {
  score: 78,
  total: 100,
  label: 'Job Readiness',
  description: 'Based on your current skills, projects and target role.',
  level: 'Competitive Candidate',
  breakdown: [
    { label: 'Technical Mastery', score: 82 },
    { label: 'Industry Relevance', score: 76 },
    { label: 'Portfolio Coverage', score: 74 },
  ],
}

export const mockSkillProfile = [
  { name: 'Python', level: 90, category: 'Programming' },
  { name: 'SQL', level: 85, category: 'Database' },
  { name: 'Power BI', level: 80, category: 'Visualization' },
  { name: 'Excel', level: 72, category: 'Analytics' },
  { name: 'Machine Learning', level: 65, category: 'Data Science' },
]

export const mockSkillGaps = [
  {
    name: 'Statistics',
    currentLevel: 55,
    targetLevel: 85,
    priority: 'High Priority',
    notes: 'Hypothesis testing & regression',
  },
  {
    name: 'Advanced SQL',
    currentLevel: 45,
    targetLevel: 80,
    priority: 'High Priority',
    notes: 'Window functions & CTE optimization',
  },
  {
    name: 'Tableau',
    currentLevel: 35,
    targetLevel: 75,
    priority: 'Medium Priority',
    notes: 'Calculated fields & dashboard publishing',
  },
  {
    name: 'Data Storytelling',
    currentLevel: 30,
    targetLevel: 70,
    priority: 'Medium Priority',
    notes: 'Executive summaries & insight framing',
  },
]

export const mockCareerRoles = [
  {
    title: 'Data Analyst',
    matchPercentage: 92,
    salaryRange: '$75k - $95k',
    demand: 'Very High',
    primaryFit: 'Strong SQL, Python & Visualization overlap',
  },
  {
    title: 'BI Analyst',
    matchPercentage: 87,
    salaryRange: '$80k - $105k',
    demand: 'High',
    primaryFit: 'Power BI & dimensional data modeling focus',
  },
  {
    title: 'Business Analyst',
    matchPercentage: 84,
    salaryRange: '$70k - $90k',
    demand: 'High',
    primaryFit: 'Excel & analytical business translation',
  },
  {
    title: 'Junior Data Scientist',
    matchPercentage: 71,
    salaryRange: '$85k - $110k',
    demand: 'Moderate',
    primaryFit: 'Requires stronger statistical modeling foundation',
  },
]

export const mockRoadmap = [
  {
    week: 'Week 1',
    topic: 'Advanced SQL',
    status: 'In Progress',
    detail: 'Window functions, partitioning, and complex subqueries',
    badge: 'Current Focus',
  },
  {
    week: 'Week 2',
    topic: 'Statistics',
    status: 'Upcoming',
    detail: 'Inferential statistics, A/B testing fundamentals',
    badge: 'Core Skill',
  },
  {
    week: 'Week 3',
    topic: 'Tableau',
    status: 'Upcoming',
    detail: 'Interactive dashboards, visual best practices',
    badge: 'Tooling',
  },
  {
    week: 'Week 4',
    topic: 'Portfolio Project',
    status: 'Upcoming',
    detail: 'End-to-end data pipeline & executive presentation',
    badge: 'Capstone',
  },
]

export const mockRecentActivity = [
  {
    id: 'act-1',
    action: 'Resume analyzed',
    detail: 'Resume uploaded & parsed against target roles',
    timestamp: '2 hours ago',
    type: 'analysis',
  },
  {
    id: 'act-2',
    action: 'Data Analyst role analyzed',
    detail: 'Market criteria benchmarked across 240+ job descriptions',
    timestamp: '5 hours ago',
    type: 'benchmark',
  },
  {
    id: 'act-3',
    action: 'Skill gap identified',
    detail: 'Identified 4 growth areas for senior trajectory',
    timestamp: '1 day ago',
    type: 'gap',
  },
  {
    id: 'act-4',
    action: 'Learning roadmap generated',
    detail: 'Personalized 4-week structured curriculum prepared',
    timestamp: '2 days ago',
    type: 'roadmap',
  },
]
