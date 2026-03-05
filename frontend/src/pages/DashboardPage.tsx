import React from 'react';
import { useDashboard, useTrends, useBreakdown, useEcoTips } from '../services/api';
import { CarbonGauge, TrendChart, CategoryBreakdown as CategoryBreakdownChart } from '../components';
import { formatCarbon } from '../utils';

export default function DashboardPage() {
  const { data: overview, isLoading: loadingOverview } = useDashboard();
  const { data: trends } = useTrends();
  const { data: breakdown } = useBreakdown();
  const { data: tips } = useEcoTips();

  if (loadingOverview) {
    return (
      <div className="p-6 space-y-6">
        <div className="animate-pulse">
          <div className="bg-surface-tertiary rounded-xl h-32 mb-6" />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
            {[1, 2, 3, 4].map((i) => <div key={i} className="bg-surface-tertiary rounded-lg h-28" />)}
          </div>
        </div>
      </div>
    );
  }

  if (!overview) {
    return (
      <div className="p-6">
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md p-4">
          <h3 className="text-sm font-medium text-red-800 dark:text-red-300">Erreur de chargement</h3>
          <p className="mt-2 text-sm text-red-700 dark:text-red-400">Impossible de charger le tableau de bord</p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-800 rounded-xl p-6 text-white">
        <h2 className="text-xl font-bold">Bienvenue sur EcoTrack</h2>
        <p className="text-primary-100 mt-1">Suivez et reduisez votre empreinte carbone au quotidien</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-5">
          <p className="text-sm text-content-tertiary">Carbone aujourd'hui</p>
          <p className="text-2xl font-bold text-content-primary mt-1">{formatCarbon(overview.total_carbon_today)}</p>
        </div>
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-5">
          <p className="text-sm text-content-tertiary">Cette semaine</p>
          <p className="text-2xl font-bold text-content-primary mt-1">{formatCarbon(overview.total_carbon_week)}</p>
        </div>
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-5">
          <p className="text-sm text-content-tertiary">Eco Score</p>
          <p className="text-2xl font-bold text-primary-600 dark:text-primary-400 mt-1">{overview.eco_score}</p>
        </div>
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-5">
          <p className="text-sm text-content-tertiary">Streak</p>
          <p className="text-2xl font-bold text-primary-600 dark:text-primary-400 mt-1">{overview.streak_days} jours</p>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
          <h3 className="text-lg font-semibold text-content-primary mb-4">Empreinte du mois</h3>
          <div className="flex justify-center">
            <CarbonGauge value={overview.total_carbon_month} />
          </div>
        </div>

        {breakdown && (
          <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
            <h3 className="text-lg font-semibold text-content-primary mb-4">Repartition par categorie</h3>
            <CategoryBreakdownChart breakdown={breakdown} />
          </div>
        )}
      </div>

      {/* Trends */}
      {trends && (
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
          <h3 className="text-lg font-semibold text-content-primary mb-4">Tendances de la semaine</h3>
          <TrendChart trend={trends} />
        </div>
      )}

      {/* Eco Tips */}
      {tips && tips.length > 0 && (
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
          <h3 className="text-lg font-semibold text-content-primary mb-4">Eco-conseils</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {tips.slice(0, 4).map((tip, i) => (
              <div key={i} className="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-4">
                <h4 className="font-medium text-primary-800 dark:text-primary-200">{tip.title}</h4>
                <p className="text-sm text-primary-700 dark:text-primary-300 mt-1">{tip.description}</p>
                <p className="text-xs text-primary-600 dark:text-primary-400 mt-2">Economie potentielle: {formatCarbon(tip.potential_savings_kg)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
