import { Agent } from '../lib/api';
import { User, Calendar, Users } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { motion } from 'framer-motion';

interface AgentCardProps {
  agent: Agent;
  index: number;
}

// Gender icon and color mapping
const genderConfig = {
  Male: { color: 'bg-blue-100 text-blue-700 border-blue-200' },
  Female: { color: 'bg-pink-100 text-pink-700 border-pink-200' },
  'Non-binary': { color: 'bg-purple-100 text-purple-700 border-purple-200' }
};

export function AgentCard({ agent, index }: AgentCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <Card className="h-full">
        <CardHeader className="pb-3">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0">
              <User className="w-5 h-5 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <CardTitle className="text-base">{agent.name}</CardTitle>
              {/* Age and Gender Chips */}
              {(agent.age || agent.gender) && (
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {agent.age && (
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full bg-gray-100 text-gray-700 border border-gray-200">
                      <Calendar className="w-3 h-3" />
                      {agent.age} yrs
                    </span>
                  )}
                  {agent.gender && (
                    <span className={`inline-flex items-center gap-1 px-2 py-0.5 text-xs font-medium rounded-full border ${genderConfig[agent.gender]?.color || 'bg-gray-100 text-gray-700 border-gray-200'}`}>
                      <Users className="w-3 h-3" />
                      {agent.gender}
                    </span>
                  )}
                </div>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          <div>
            <p className="text-sm text-foreground/90">{agent.description}</p>
          </div>
          <div className="pt-2 border-t border-border">
            <p className="text-xs text-muted-foreground mb-1">Reasoning:</p>
            <p className="text-xs text-foreground/80 italic">{agent.reasoning}</p>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}
