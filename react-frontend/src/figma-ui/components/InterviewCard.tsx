import { Interview } from '../lib/api';
import { MessageSquare } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { motion } from 'framer-motion';

interface InterviewCardProps {
  interview: Interview;
  index: number;
}

export function InterviewCard({ interview, index }: InterviewCardProps) {
  const firstQA = interview.interview[0];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <Card>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-primary" />
              <CardTitle className="text-sm">Agent {interview.agent_id + 1} Interview</CardTitle>
            </div>
            <span className="text-xs text-muted-foreground">
              {interview.interview.length} Q&A
            </span>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="space-y-2">
            <div className="text-xs">
              <p className="text-muted-foreground mb-1">Q: {firstQA.question}</p>
              <p className="text-foreground/80 pl-3 border-l-2 border-primary/30">
                {firstQA.answer}
              </p>
            </div>
          </div>
          {interview.interview.length > 1 && (
            <p className="text-xs text-muted-foreground">
              + {interview.interview.length - 1} more questions
            </p>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
