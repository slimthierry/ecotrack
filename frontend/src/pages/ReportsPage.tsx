import React, { useState } from 'react';
import { useWeeklyReport, useMonthlyReport } from '../services/api';
import { formatCarbon } from '../utils';

type ReportTab = 'weekly' | 'monthly';

export default function ReportsPage() {
  const [tab, setTab] = useState<ReportTab>('weekly');
  const { data: weeklyReport, isLoading: loadingWeekly } = useWeeklyReport();
  const { data: monthlyReport, isLoading: loadingMonthly } = useMonthlyReport();

  const isLoading = tab === 'weekly' ? loadingWeekly : loadingMonthly;
  const report = tab === 'weekly' ? weeklyReport : monthlyReport;

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold text-content-primary">Rapports</h2>

      {/* Tab Selector */}
      <div className="inline-flex rounded-lg border border-edge-primary bg-surface-primary p-1">
        <button
          onClick={() => setTab('weekly')}
          className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
            tab === 'weekly' ? 'bg-primary-500 text-white' : 'text-content-secondary hover:bg-surface-tertiary'
          }`}
        >
          Hebdomadaire
        </button>
        <button
          onClick={() => setTab('monthly')}
          className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
            tab === 'monthly' ? 'bg-primary-500 text-white' : 'text-content-secondary hover:bg-surface-tertiary'
          }`}
        >
          Mensuel
        </button>
      </div>

      {isLoading ? (
        <div className="animate-pulse space-y-4">
          <div className="bg-surface-tertiary rounded-lg h-40" />
          <div className="bg-surface-tertiary rounded-lg h-60" />
        </div>
      ) : report ? (
        <div className="space-y-6">
          {/* Summary */}
          <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
            <h3 className="text-lg font-semibold text-content-primary mb-4">Resume</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
              <div>
                <p className="text-sm text-content-tertiary">Carbone total</p>
                <p className="text-xl font-bold text-content-primary">{report.summary.total_carbon_formatted}</p>
              </div>
              <div>
                <p className="text-sm text-content-tertiary">Activites</p>
                <p className="text-xl font-bold text-content-primary">{report.summary.activity_count}</p>
              </div>
              <div>
                <p className="text-sm text-content-tertiary">Moyenne quotidienne</p>
                <p className="text-xl font-bold text-content-primary">{formatCarbon(report.summary.daily_average_kg)}</p>
              </div>
              <div>
                <p className="text-sm text-content-tertiary">Equivalent arbres</p>
                <p className="text-xl font-bold text-primary-600 dark:text-primary-400">{report.summary.trees_equivalent.toFixed(1)}</p>
              </div>
              <div>
                <p className="text-sm text-content-tertiary">Equivalent km en voiture</p>
                <p className="text-xl font-bold text-content-primary">{report.summary.driving_km_equivalent.toFixed(0)} km</p>
              </div>
            </div>
          </div>

          {/* Comparison */}
          {report.comparison?.vs_average && (
            <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
              <h3 className="text-lg font-semibold text-content-primary mb-4">Comparaison</h3>
              <div className="flex items-center gap-4">
                <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                  report.comparison.vs_average.level === 'low'
                    ? 'bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400'
                    : report.comparison.vs_average.level === 'medium'
                    ? 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-400'
                    : 'bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400'
                }`}>
                  {report.comparison.vs_average.level === 'low' ? 'En dessous de la moyenne' :
                   report.comparison.vs_average.level === 'medium' ? 'Dans la moyenne' : 'Au dessus de la moyenne'}
                </div>
              </div>
              <p className="text-sm text-content-secondary mt-3">{report.comparison.vs_average.message}</p>
            </div>
          )}

          {/* Category Breakdown */}
          {report.category_breakdown && (
            <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
              <h3 className="text-lg font-semibold text-content-primary mb-4">Repartition par categorie</h3>
              <div className="space-y-3">
                {Object.entries(report.category_breakdown).map(([category, value]) => (
                  <div key={category} className="flex items-center justify-between">
                    <span className="text-sm font-medium text-content-secondary capitalize">{category}</span>
                    <span className="text-sm text-content-secondary">{formatCarbon(value as number)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-content-tertiary">Pas assez de donnees pour generer un rapport. Commencez par enregistrer des activites.</p>
        </div>
      )}
    </div>
  );
}
