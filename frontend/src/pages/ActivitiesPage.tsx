import React, { useState } from 'react';
import { useActivities, useCreateActivity, useDeleteActivity } from '../services/api';
import { ActivityCard } from '../components';
import type { ActivityCategory, ActivityCreate } from '../types';

const categories: { value: ActivityCategory; label: string }[] = [
  { value: 'transport', label: 'Transport' },
  { value: 'food', label: 'Alimentation' },
  { value: 'energy', label: 'Energie' },
  { value: 'purchase', label: 'Achats' },
];

export default function ActivitiesPage() {
  const [filterCategory, setFilterCategory] = useState<string>('');
  const { data: activities, isLoading } = useActivities(
    filterCategory ? { category: filterCategory } : undefined,
  );
  const createMutation = useCreateActivity();
  const deleteMutation = useDeleteActivity();
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState<ActivityCreate>({
    category: 'transport',
    sub_category: '',
    quantity: 0,
    unit: 'km',
    date: new Date().toISOString().split('T')[0],
  });

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    await createMutation.mutateAsync(form);
    setShowForm(false);
    setForm({ category: 'transport', sub_category: '', quantity: 0, unit: 'km', date: new Date().toISOString().split('T')[0] });
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-bold text-content-primary">Activites</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 transition-colors text-sm font-medium"
        >
          {showForm ? 'Annuler' : '+ Nouvelle activite'}
        </button>
      </div>

      {/* Create Form */}
      {showForm && (
        <div className="bg-surface-primary rounded-xl border border-edge-primary p-6">
          <h3 className="text-lg font-semibold text-content-primary mb-4">Ajouter une activite</h3>
          <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-content-secondary mb-1">Categorie</label>
              <select
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value as ActivityCategory })}
                className="input-field"
              >
                {categories.map((c) => (
                  <option key={c.value} value={c.value}>{c.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-content-secondary mb-1">Sous-categorie</label>
              <input
                type="text"
                value={form.sub_category}
                onChange={(e) => setForm({ ...form, sub_category: e.target.value })}
                className="input-field"
                placeholder="ex: voiture, bus..."
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-content-secondary mb-1">Quantite</label>
              <input
                type="number"
                value={form.quantity}
                onChange={(e) => setForm({ ...form, quantity: Number(e.target.value) })}
                className="input-field"
                min="0"
                step="0.1"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-content-secondary mb-1">Unite</label>
              <input
                type="text"
                value={form.unit}
                onChange={(e) => setForm({ ...form, unit: e.target.value })}
                className="input-field"
                placeholder="km, kg, kWh..."
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-content-secondary mb-1">Date</label>
              <input
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
                className="input-field"
                required
              />
            </div>
            <div className="flex items-end">
              <button
                type="submit"
                disabled={createMutation.isPending}
                className="w-full py-2 px-4 bg-primary-600 text-white font-medium rounded-md hover:bg-primary-700 disabled:opacity-50 transition-colors"
              >
                {createMutation.isPending ? 'Ajout...' : 'Ajouter'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Filter */}
      <div className="flex gap-2">
        <button
          onClick={() => setFilterCategory('')}
          className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
            !filterCategory ? 'bg-primary-500 text-white' : 'bg-surface-primary text-content-secondary border border-edge-primary hover:bg-surface-secondary'
          }`}
        >
          Tout
        </button>
        {categories.map((c) => (
          <button
            key={c.value}
            onClick={() => setFilterCategory(c.value)}
            className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors ${
              filterCategory === c.value ? 'bg-primary-500 text-white' : 'bg-surface-primary text-content-secondary border border-edge-primary hover:bg-surface-secondary'
            }`}
          >
            {c.label}
          </button>
        ))}
      </div>

      {/* Activities List */}
      {isLoading ? (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => <div key={i} className="bg-surface-tertiary animate-pulse rounded-lg h-20" />)}
        </div>
      ) : activities && activities.length > 0 ? (
        <div className="space-y-3">
          {activities.map((activity) => (
            <ActivityCard
              key={activity.id}
              activity={activity}
              onDelete={() => deleteMutation.mutate(activity.id)}
            />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-content-tertiary">Aucune activite enregistree. Commencez par en ajouter une!</p>
        </div>
      )}
    </div>
  );
}
