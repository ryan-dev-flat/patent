import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const PatentScoreChart = ({ utility, novelty, obviousness, patentability, chartType }) => {
  const data = [
    { name: 'Utility', weighted: utility.utility_score || 0 },
    { name: 'Novelty', weighted: novelty.novelty_score || 0 },
    { name: 'Non-Obviousness', weighted: obviousness.obviousness_score || 0 },
    { name: 'Patentability Overall', weighted: patentability.patentability_score || 0 },
  ];

  const renderRadarChart = () => (
    <RadarChart cx="50%" cy="50%" outerRadius="80%" data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="name" />
      <PolarRadiusAxis angle={30} domain={[0, 1]} />
      <Radar name="Patent Scores" dataKey="weighted" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
    </RadarChart>
  );

  const renderBarChart = () => (
    <BarChart data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis domain={[0, 1]} />
      <Tooltip />
      <Legend />
      <Bar dataKey="weighted" fill="#8884d8" />
    </BarChart>
  );

  const renderPieChart = () => (
    <PieChart>
      <Pie
        data={data}
        cx="50%"
        cy="50%"
        labelLine={false}
        outerRadius={80}
        fill="#8884d8"
        dataKey="weighted"
      >
        {data.map((entry, index) => (
          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
        ))}
      </Pie>
      <Tooltip />
      <Legend />
    </PieChart>
  );

  const renderChart = () => {
    switch (chartType) {
      case 'radar':
        return renderRadarChart();
      case 'bar':
        return renderBarChart();
      case 'pie':
        return renderPieChart();
      default:
        return renderRadarChart();
    }
  };

  return (
    <ResponsiveContainer width="100%" height={300}>
      {renderChart()}
    </ResponsiveContainer>
  );
};

export default PatentScoreChart;