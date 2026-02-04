import React, { useState } from 'react';
import { Agent } from '../lib/api';
import { Badge } from './ui/badge';
import { Quote, Target, TrendingUp, AlertCircle } from 'lucide-react';

interface PersonaProfileProps {
  agent: Agent;
}

function getInitials(name: string): string {
  return name
    .split(/[\s,]+/)
    .map((s) => s.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

// Avatar URL from DiceBear (person-style avatars); fallback to initials if image fails
function getAvatarUrl(name: string): string {
  const seed = encodeURIComponent(name || 'Agent');
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${seed}&backgroundColor=b6e3f4,c0aede,d1d4f9`;
}

export function PersonaProfile({ agent }: PersonaProfileProps) {
  const [avatarError, setAvatarError] = useState(false);
  const showAvatar = !avatarError;

  const firstSentence = agent.description.split('.')[0];
  const quoteText = agent.quote ?? (firstSentence ? `${firstSentence}.` : '');

  // Always use Goals, Motivations, Pain Points in bullet format; derive from description sentences if missing
  const descSentences = agent.description
    .replace(/\n/g, ' ')
    .split(/(?<=[.!])\s+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 10);
  const goals = agent.goals?.length ? agent.goals : descSentences.slice(0, 3);
  const motivations = agent.motivations?.length ? agent.motivations : descSentences.slice(3, 6);
  const painPoints = agent.painPoints?.length ? agent.painPoints : descSentences.slice(6, 9);

  // Demographics: chip 1 = "34, Female", chip 2 (beneath) = "San Diego, CA"
  const ageGender = [agent.age != null ? `${agent.age}` : null, agent.gender ?? null]
    .filter(Boolean)
    .join(', ');
  const location = agent.location?.trim() || null;

  return (
    <div className="bg-card rounded-xl overflow-hidden border border-border p-6 shadow-sm max-w-4xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left: Avatar, name, occupation, demographics */}
        <div className="lg:col-span-4 flex flex-col items-center text-center space-y-4">
          <div className="relative">
            <div className="absolute inset-0 bg-primary/10 rounded-full scale-110 -rotate-6" />
            <div className="relative w-32 h-32 rounded-full overflow-hidden border-4 border-background shadow-xl bg-primary/10 flex items-center justify-center">
              {showAvatar ? (
                <img
                  src={getAvatarUrl(agent.name)}
                  alt={agent.name}
                  className="w-full h-full object-cover"
                  onError={() => setAvatarError(true)}
                />
              ) : (
                <span className="text-3xl font-bold text-primary">
                  {getInitials(agent.name)}
                </span>
              )}
            </div>
          </div>
          <div>
            <h3 className="text-2xl font-bold tracking-tight mb-1">{agent.name}</h3>
            {agent.occupation && (
              <p className="text-lg font-semibold text-primary">{agent.occupation}</p>
            )}
            <div className="flex flex-col items-center gap-1.5 mt-2">
              {ageGender && (
                <Badge variant="secondary" className="font-normal">
                  {ageGender}
                </Badge>
              )}
              {location && (
                <Badge variant="outline" className="font-normal">
                  {location}
                </Badge>
              )}
            </div>
          </div>
        </div>

        {/* Right: Quote + Goals / Motivations / Pain Points (always in bullet format) */}
        <div className="lg:col-span-8 space-y-6">
          {quoteText && (
            <div className="relative bg-primary/5 p-6 rounded-2xl border-l-4 border-primary italic text-base leading-relaxed">
              <Quote className="absolute -top-2 -left-1 w-6 h-6 text-primary opacity-20" />
              &ldquo;{quoteText}.&rdquo;
            </div>
          )}

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400">
                <Target className="w-4 h-4 shrink-0" />
                <span className="font-semibold text-xs uppercase tracking-wider">Goals</span>
              </div>
              <ul className="space-y-2">
                {goals.length ? goals.map((goal, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-foreground/90">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0" />
                    {goal}
                  </li>
                )) : (
                  <li className="flex items-start gap-2 text-sm text-muted-foreground">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0" />
                    —
                  </li>
                )}
              </ul>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-amber-600 dark:text-amber-400">
                <TrendingUp className="w-4 h-4 shrink-0" />
                <span className="font-semibold text-xs uppercase tracking-wider">Motivations</span>
              </div>
              <ul className="space-y-2">
                {motivations.length ? motivations.map((mot, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-foreground/90">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
                    {mot}
                  </li>
                )) : (
                  <li className="flex items-start gap-2 text-sm text-muted-foreground">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-amber-500 shrink-0" />
                    —
                  </li>
                )}
              </ul>
            </div>
            <div className="space-y-3">
              <div className="flex items-center gap-2 text-rose-600 dark:text-rose-400">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span className="font-semibold text-xs uppercase tracking-wider">Pain Points</span>
              </div>
              <ul className="space-y-2">
                {painPoints.length ? painPoints.map((pain, i) => (
                  <li key={i} className="flex items-start gap-2 text-sm text-foreground/90">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0" />
                    {pain}
                  </li>
                )) : (
                  <li className="flex items-start gap-2 text-sm text-muted-foreground">
                    <span className="mt-1.5 w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0" />
                    —
                  </li>
                )}
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Footer: System Reasoning (one liner) */}
      {agent.reasoning && (
        <div className="mt-8 pt-6 border-t border-border">
          <p className="text-xs text-muted-foreground uppercase tracking-widest font-semibold mb-1">
            System Reasoning
          </p>
          <p className="text-sm text-muted-foreground italic truncate" title={agent.reasoning}>
            {(() => {
              const first = agent.reasoning.split(/[.!]/)[0]?.trim().replace(/\s+/g, ' ');
              return (first && first.length > 0 ? first + '.' : agent.reasoning.slice(0, 120).trim());
            })()}
          </p>
        </div>
      )}
    </div>
  );
}
