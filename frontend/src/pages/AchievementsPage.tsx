import React from 'react';
import { useAchievements, useUserAchievements } from '../services/api';
import { AchievementCard } from '../components';

export default function AchievementsPage() {
  const { data: achievements, isLoading } = useAchievements();
  const { data: userAchievements } = useUserAchievements();

  const unlockedIds = new Set(userAchievements?.map((ua) => ua.achievement.id) || []);

  if (isLoading) {
    return (
      <div className="p-6 space-y-6">
        <div className="animate-pulse grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => <div key={i} className="bg-surface-tertiary rounded-lg h-40" />)}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-content-primary">Achievements</h2>
        <span className="text-sm text-content-tertiary">
          {userAchievements?.length || 0} / {achievements?.length || 0} debloques
        </span>
      </div>

      {/* Unlocked */}
      {userAchievements && userAchievements.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-content-primary mb-3">Debloques</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {userAchievements.map((ua) => (
              <AchievementCard
                key={ua.id}
                achievement={ua.achievement}
                unlocked
                unlockedAt={ua.unlocked_at}
              />
            ))}
          </div>
        </div>
      )}

      {/* Locked */}
      {achievements && achievements.filter((a) => !unlockedIds.has(a.id)).length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-content-primary mb-3">A debloquer</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {achievements
              .filter((a) => !unlockedIds.has(a.id))
              .map((achievement) => (
                <AchievementCard
                  key={achievement.id}
                  achievement={achievement}
                  unlocked={false}
                />
              ))}
          </div>
        </div>
      )}

      {!achievements || achievements.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-content-tertiary">Aucun achievement disponible.</p>
        </div>
      ) : null}
    </div>
  );
}
