import React, { useState } from 'react';
import { useChallenges, useMyChallenges, useJoinChallenge, useLeaderboard } from '../services/api';
import { ChallengeCard } from '../components';
import { formatCarbon } from '../utils';

export default function ChallengesPage() {
  const { data: challenges, isLoading } = useChallenges();
  const { data: myChallenges } = useMyChallenges();
  const joinMutation = useJoinChallenge();
  const [selectedChallenge, setSelectedChallenge] = useState<string>('');
  const { data: leaderboard } = useLeaderboard(selectedChallenge);

  if (isLoading) {
    return (
      <div className="p-6 space-y-6">
        <div className="animate-pulse space-y-4">
          {[1, 2, 3].map((i) => <div key={i} className="bg-surface-tertiary rounded-lg h-32" />)}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <h2 className="text-xl font-bold text-content-primary">Challenges</h2>

      {/* My Challenges */}
      {myChallenges && myChallenges.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-content-primary mb-3">Mes challenges en cours</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {myChallenges.map((progress) => (
              <div key={progress.challenge_id} className="bg-surface-primary rounded-xl border border-edge-primary p-5">
                <h4 className="font-medium text-content-primary">{progress.challenge_title}</h4>
                <div className="mt-3">
                  <div className="flex justify-between text-sm text-content-secondary mb-1">
                    <span>Progression</span>
                    <span>{Math.round(progress.progress_percent)}%</span>
                  </div>
                  <div className="w-full bg-surface-tertiary rounded-full h-2">
                    <div
                      className="bg-primary-500 h-2 rounded-full transition-all"
                      style={{ width: `${Math.min(progress.progress_percent, 100)}%` }}
                    />
                  </div>
                </div>
                <div className="flex justify-between mt-3 text-sm">
                  <span className="text-primary-600 dark:text-primary-400">{formatCarbon(progress.carbon_saved)} economises</span>
                  <span className="text-content-tertiary">{progress.days_remaining}j restants</span>
                </div>
                <button
                  onClick={() => setSelectedChallenge(progress.challenge_id)}
                  className="mt-3 text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 font-medium"
                >
                  Voir le classement
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Available Challenges */}
      <div>
        <h3 className="text-lg font-semibold text-content-primary mb-3">Challenges disponibles</h3>
        {challenges && challenges.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {challenges.map((challenge) => (
              <ChallengeCard
                key={challenge.id}
                challenge={challenge}
                onJoin={() => joinMutation.mutate({ challenge_id: challenge.id })}
              />
            ))}
          </div>
        ) : (
          <p className="text-content-tertiary text-sm">Aucun challenge disponible pour le moment.</p>
        )}
      </div>

      {/* Leaderboard */}
      {selectedChallenge && leaderboard && (
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-content-primary">Classement</h3>
            <button
              onClick={() => setSelectedChallenge('')}
              className="text-sm text-content-tertiary hover:text-content-secondary"
            >
              Fermer
            </button>
          </div>
          <div className="space-y-2">
            {leaderboard.map((entry) => (
              <div key={entry.rank} className="flex items-center justify-between py-2 border-b border-edge-secondary last:border-0">
                <div className="flex items-center gap-3">
                  <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    entry.rank <= 3 ? 'bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300' : 'bg-surface-tertiary text-content-secondary'
                  }`}>
                    {entry.rank}
                  </span>
                  <span className="font-medium text-content-primary">{entry.username}</span>
                </div>
                <span className="text-sm text-primary-600 dark:text-primary-400 font-medium">{formatCarbon(entry.carbon_saved)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
