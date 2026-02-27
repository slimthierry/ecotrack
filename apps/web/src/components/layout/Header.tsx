import React from 'react';
import { useCurrentUser } from '@ecotrack/api-client';
import { ThemeToggleIcon } from '@ecotrack/theme';

export function Header() {
  const { data: user } = useCurrentUser();

  return (
    <header className="h-16 bg-surface-primary border-b border-edge-primary flex items-center justify-between px-6">
      <div>
        <h1 className="text-lg font-semibold text-content-primary">EcoTrack</h1>
      </div>
      <div className="flex items-center gap-4">
        {user && (
          <div className="flex items-center gap-2">
            <span className="text-sm text-content-secondary">Score: {user.eco_score}</span>
            <span className="text-sm text-primary-600 dark:text-primary-400 font-medium">{user.streak_days}j streak</span>
          </div>
        )}
        <ThemeToggleIcon />
        <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900/30 rounded-full flex items-center justify-center">
          <span className="text-primary-700 dark:text-primary-300 font-medium text-sm">
            {user?.username?.[0]?.toUpperCase() || 'U'}
          </span>
        </div>
      </div>
    </header>
  );
}
