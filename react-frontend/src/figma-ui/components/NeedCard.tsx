import { useState } from 'react';
import { Need } from '../lib/api';
import { Badge } from './ui/badge';
import { Card, CardContent } from './ui/card';
import { motion } from 'framer-motion';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface NeedCardProps {
  need: Need;
  index: number;
}

const categoryColors: Record<Need['category'], string> = {
  Functional: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  Usability: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  Performance: 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200',
  Safety: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  Emotional: 'bg-pink-100 text-pink-800 dark:bg-pink-900 dark:text-pink-200',
  Social: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
  Accessibility: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200',
};

const priorityColors: Record<Need['priority'], string> = {
  High: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
  Medium: 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200',
  Low: 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200',
};

export function NeedCard({ need, index }: NeedCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
    >
      <Card 
        className="h-full hover:shadow-md transition-shadow cursor-pointer" 
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <CardContent className="p-4 space-y-3">
          <div className="flex items-start justify-between gap-2">
            <div className="flex items-start gap-2 flex-wrap">
              <Badge className={`text-xs ${categoryColors[need.category]}`} variant="secondary">
                {need.category}
              </Badge>
              <Badge className={`text-xs ${priorityColors[need.priority]}`} variant="secondary">
                {need.priority}
              </Badge>
            </div>
            {isExpanded ? (
              <ChevronUp className="w-4 h-4 text-muted-foreground flex-shrink-0" />
            ) : (
              <ChevronDown className="w-4 h-4 text-muted-foreground flex-shrink-0" />
            )}
          </div>
          <p className="text-sm font-medium">{need.need_statement}</p>
          
          {isExpanded && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
              className="space-y-3 pt-2 border-t"
            >
              {need.evidence && (
                <div>
                  <p className="text-xs font-semibold text-muted-foreground mb-1">Evidence</p>
                  <p className="text-xs text-foreground/80">{need.evidence}</p>
                </div>
              )}
              {need.design_implication && (
                <div>
                  <p className="text-xs font-semibold text-muted-foreground mb-1">Design Implications</p>
                  <p className="text-xs text-foreground/80">{need.design_implication}</p>
                </div>
              )}
            </motion.div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
