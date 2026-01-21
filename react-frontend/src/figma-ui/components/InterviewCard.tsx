import { useState } from 'react';
import { Interview } from '../lib/api';
import { MessageSquare, ChevronDown, ChevronUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { motion } from 'framer-motion';

interface InterviewCardProps {
  interview: Interview;
  index: number;
}

export function InterviewCard({ interview, index }: InterviewCardProps) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getInterviewSummary = () => {
    const topics: string[] = [];
    interview.interview.forEach(qa => {
      const q = qa.question.toLowerCase();
      if (q.includes('challeng')) topics.push('Challenges');
      if (q.includes('improve') || q.includes('better')) topics.push('Improvements');
      if (q.includes('feature') || q.includes('function')) topics.push('Features');
      if (q.includes('frustrat') || q.includes('issue')) topics.push('Pain Points');
      if (q.includes('workflow') || q.includes('process')) topics.push('Workflow');
      if (q.includes('goal') || q.includes('objective')) topics.push('Goals');
    });
    const uniqueTopics = [...new Set(topics)];
    return uniqueTopics.length > 0 
      ? `Discussed ${uniqueTopics.slice(0, 3).join(', ')}`
      : 'Interview completed';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
    >
      <Card className="cursor-pointer hover:shadow-md transition-shadow" onClick={() => setIsExpanded(!isExpanded)}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-primary" />
              <CardTitle className="text-sm">Agent {interview.agent_id} Interview</CardTitle>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="secondary" className="text-xs">
                {interview.interview.length} Q&A
              </Badge>
              {isExpanded ? (
                <ChevronUp className="w-4 h-4 text-muted-foreground" />
              ) : (
                <ChevronDown className="w-4 h-4 text-muted-foreground" />
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          {!isExpanded ? (
            <p className="text-sm text-muted-foreground">{getInterviewSummary()}</p>
          ) : (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.2 }}
              className="space-y-4"
            >
              {interview.interview.map((qa, idx) => (
                <div key={idx} className="space-y-2 pb-3 border-b last:border-b-0 last:pb-0">
                  <p className="text-xs font-medium text-muted-foreground">Q{idx + 1}: {qa.question}</p>
                  <p className="text-xs text-foreground/80 pl-3 border-l-2 border-primary/30">
                    {qa.answer}
                  </p>
                </div>
              ))}
            </motion.div>
          )}
        </CardContent>
      </Card>
    </motion.div>
  );
}
