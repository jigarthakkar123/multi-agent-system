import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid
} from 'recharts';
import { Building2, PieChart as PieIcon, LineChart as ChartIcon, MapPin, Receipt } from 'lucide-react';

const COLORS = ['#6366F1', '#38BDF8', '#10B981', '#F59E0B', '#F43F5E', '#A855F7', '#EC4899', '#14B8A6'];

export default function AnalyticsView({
  monthlyTrends,
  cityPerformance,
  propertyTypes,
  expenseBreakdown
}) {
  const formatYAxisCr = (tick) => `₹${(tick / 10000000).toFixed(0)}Cr`;
  const formatYAxisL = (tick) => `₹${(tick / 100000).toFixed(0)}L`;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
        <div>
          <h2 className="text-base font-bold text-white">Market & Financial Performance Analytics</h2>
          <p className="text-xs text-slate-400">
            Real Estate transaction data coverage: May 1, 2026 – October 31, 2026 across 10 Urban Centers
          </p>
        </div>
        <div className="flex items-center gap-2 text-xs text-indigo-400 font-mono bg-indigo-500/10 px-3 py-1.5 rounded-xl border border-indigo-500/20">
          <span>6 Months Completed</span>
        </div>
      </div>

      {/* Row 1: Monthly Trends & Expense Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Net Profit & Commission */}
        <div className="lg:col-span-2 glass-card p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <ChartIcon className="w-4 h-4 text-emerald-400" />
              <h3 className="text-sm font-bold text-white">Commission Earnings vs. Operational Expenses</h3>
            </div>
            <div className="text-xs text-slate-400">Monthly Cash Flow Audit</div>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={monthlyTrends} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
                <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} tickFormatter={formatYAxisL} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }}
                  formatter={(v, name) => [`₹${(v / 100000).toFixed(2)} Lakhs`, name === 'commission' ? 'Commissions Earned' : 'Operating Expenses']}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="commission" name="Brokerage Commission" fill="#10B981" radius={[4, 4, 0, 0]} />
                <Bar dataKey="expenses" name="Operating Expenses" fill="#F43F5E" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Expense Category Pie */}
        <div className="glass-card p-5 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Receipt className="w-4 h-4 text-rose-400" />
                <h3 className="text-sm font-bold text-white">Expense Distribution</h3>
              </div>
              <span className="text-xs text-slate-400">By Category</span>
            </div>

            <div className="h-56 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={expenseBreakdown || []}
                    dataKey="amount"
                    nameKey="category"
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={3}
                  >
                    {expenseBreakdown && expenseBreakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', color: '#FFF' }}
                    formatter={(v, name) => [`₹${(v / 100000).toFixed(2)} Lakhs`, name]}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="space-y-1.5 pt-2 border-t border-slate-800 text-xs">
            {expenseBreakdown && expenseBreakdown.slice(0, 4).map((item, idx) => (
              <div key={idx} className="flex items-center justify-between text-slate-300">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: COLORS[idx % COLORS.length] }}></span>
                  <span>{item.category}</span>
                </div>
                <span className="font-mono text-slate-400">{item.percentage}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Row 2: City Comparison & Property Type Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* City Performance Table & Chart */}
        <div className="glass-card p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <MapPin className="w-4 h-4 text-sky-400" />
              <h3 className="text-sm font-bold text-white">City Market Transaction Velocity</h3>
            </div>
            <span className="text-xs text-slate-400">10 Metros Audited</span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="py-2 px-3">City</th>
                  <th className="py-2 px-2 text-center">Listings</th>
                  <th className="py-2 px-2 text-center">Deals</th>
                  <th className="py-2 px-3 text-right">Revenue</th>
                  <th className="py-2 px-2 text-right">Conv %</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {cityPerformance && cityPerformance.map((c, i) => (
                  <tr key={i} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-2.5 px-3 font-semibold text-white">{c.city}</td>
                    <td className="py-2.5 px-2 text-center text-slate-300">{c.property_count}</td>
                    <td className="py-2.5 px-2 text-center text-emerald-400 font-medium">{c.deals_closed}</td>
                    <td className="py-2.5 px-3 text-right font-mono text-indigo-400">₹{(c.revenue_generated / 10000000).toFixed(2)} Cr</td>
                    <td className="py-2.5 px-2 text-right text-slate-300">{c.conversion_rate}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Property Type Distribution */}
        <div className="glass-card p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Building2 className="w-4 h-4 text-amber-400" />
              <h3 className="text-sm font-bold text-white">Property Type Portfolio & Absorption</h3>
            </div>
            <span className="text-xs text-slate-400">Inventory Distribution</span>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={propertyTypes || []} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
                <XAxis dataKey="property_type" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }}
                  formatter={(v, name) => [v, name === 'count' ? 'Total Listings' : 'Units Sold']}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="count" name="Total Units" fill="#6366F1" radius={[4, 4, 0, 0]} />
                <Bar dataKey="sold_count" name="Sold Units" fill="#10B981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
