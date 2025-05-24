import { PolarAngleAxis, RadialBar, RadialBarChart } from 'recharts';
import MonthSpendingChart from './MonthSpendingChart';

const data = [{ name: 'L1', value: 25 }];

const circleSize = 200;

const CerculreProgressBar = () => {
    return (
        <RadialBarChart
            width={circleSize}
            height={circleSize}
            cx={circleSize / 2}
            cy={circleSize / 2}
            innerRadius={12}
            outerRadius={18}
            barSize={2}
            data={data}
            startAngle={90}
            endAngle={-270}
        >
            <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
            <RadialBar background clockWise dataKey="value" cornerRadius={circleSize / 2} fill="#82ca9d" />
            <text x={circleSize / 2} y={circleSize / 2} textAnchor="middle" dominantBaseline="middle" className="progress-label">
                25
            </text>
        </RadialBarChart>
    );
};

export default CerculreProgressBar;
