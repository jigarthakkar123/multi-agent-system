import React from 'react';
import {
  TrendingUp,
  DollarSign,
  Receipt,
  PiggyBank,
  Users,
  Target,
  Home,
  Layers
} from 'lucide-react';

export default function KPIStats({ kpis }) {
  if (!kpis) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {[1, 2, 3, 4, 5, 6, 7, 8].map((n) => (
          <div
            key={n}
            className="p-5 rounded-2xl bg-slate-900/60 border border-slate-800 animate-pulse flex flex-col justify-between h-32"
          >
            <div className="flex justify-between items-start">
              <div className="h-4 bg-slate-800 rounded w-2/3"></div>
              <div className="h-8 w-8 bg-slate-800 rounded-xl"></div>
            </div>
            <div>
              <div className="h-6 bg-slate-700 rounded w-1/2 mb-2"></div>
              <div className="h-3 bg-slate-800 rounded w-3/4"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  const formatCurrency = (val) => {
    if (!val && val !== 0) return '₹ 0';
    if (val >= 10000000) {
      return `₹ ${(val / 10000000).toFixed(2)} Cr`;
    }
    if (val >= 100000) {
      return `₹ ${(val / 100000).toFixed(2)} L`;
    }
    return `₹ ${val.toLocaleString('en-IN')}`;
  };

  const statCards = [
    {
      title: 'Total Closed Sales Volume',
      value: formatCurrency(kpis.total_revenue),
      subtext: `${kpis.closed_won_deals} Closed Won Deals`,
      icon: DollarSign,
      color: 'from-blue-600/20 to-indigo-600/20 text-blue-400 border-blue-500/30'
    },
    {
      title: 'Total Brokerage Commission',
      value: formatCurrency(kpis.total_commission),
      subtext: 'Avg ~2.5% Commission Tier',
      icon: TrendingUp,
      color: 'from-emerald-600/20 to-teal-600/20 text-emerald-400 border-emerald-500/30'
    },
    {
      title: 'Operational Expenses',
      value: formatCurrency(kpis.total_expenses),
      subtext: 'Legal, Rent, Marketing, Travel',
      icon: Receipt,
      color: 'from-rose-600/20 to-pink-600/20 text-rose-400 border-rose-500/30'
    },
    {
      title: 'Net Agency Profit',
      value: formatCurrency(kpis.net_profit),
      subtext: `${kpis.profit_margin_pct}% Operating Margin`,
      icon: PiggyBank,
      color: 'from-amber-600/20 to-orange-600/20 text-amber-400 border-amber-500/30'
    },
    {
      title: 'Lead Conversion Rate',
      value: `${kpis.conversion_rate_pct}%`,
      subtext: `${kpis.converted_leads} of ${kpis.total_leads} Inquiries Converted`,
      icon: Users,
      color: 'from-violet-600/20 to-purple-600/20 text-violet-400 border-violet-500/30'
    },
    {
      title: 'Deal Win Rate',
      value: `${kpis.deal_win_rate_pct}%`,
      subtext: `${kpis.closed_won_deals} Closed Won of ${kpis.total_deals} Deals`,
      icon: Target,
      color: 'from-cyan-600/20 to-sky-600/20 text-cyan-400 border-cyan-500/30'
    },
    {
      title: 'Property Absorption Rate',
      value: `${kpis.absorption_rate_pct}%`,
      subtext: `${kpis.sold_inventory_units} Sold of ${kpis.total_inventory_units} Units`,
      icon: Home,
      color: 'from-indigo-600/20 to-blue-600/20 text-indigo-400 border-indigo-500/30'
    },
    {
      title: 'Avg Price per SqFt',
      value: `₹ ${Math.round(kpis.avg_property_price_sqft).toLocaleString('en-IN')}`,
      subtext: `Avg Deal: ${formatCurrency(kpis.avg_deal_size)}`,
      icon: Layers,
      color: 'from-slate-600/20 to-zinc-600/20 text-slate-300 border-slate-500/30'
    }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {statCards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            className="glass-card p-4 rounded-2xl transition-all duration-200 hover:-translate-y-0.5 hover:shadow-lg relative overflow-hidden group"
          >
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-medium text-slate-400">{card.title}</span>
              <div className={`p-2 rounded-xl bg-gradient-to-tr ${card.color} border`}>
                <Icon className="w-4 h-4" />
              </div>
            </div>
            <div className="text-xl font-bold tracking-tight text-white mb-1">
              {card.value}
            </div>
            <div className="text-[11px] text-slate-400 truncate">
              {card.subtext}
            </div>
          </div>
        );
      })}
    </div>
  );
}
