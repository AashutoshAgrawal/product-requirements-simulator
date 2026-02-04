import React, { useState } from 'react';
import { ChevronRight, ChevronDown } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from './ui/utils';

export interface TreeNodeData {
  id: string;
  label: React.ReactNode;
  icon?: React.ReactNode;
  children?: TreeNodeData[];
  content?: React.ReactNode;
  badge?: React.ReactNode;
  className?: string;
}

interface TreeViewProps {
  data: TreeNodeData[];
  defaultExpanded?: boolean;
}

export function TreeView({ data, defaultExpanded = false }: TreeViewProps) {
  return (
    <div className="space-y-1">
      {data.map((node) => (
        <TreeNode key={node.id} node={node} defaultExpanded={defaultExpanded} level={0} />
      ))}
    </div>
  );
}

function TreeNode({ node, defaultExpanded, level }: { node: TreeNodeData; defaultExpanded: boolean; level: number }) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const hasChildren = node.children && node.children.length > 0;
  const hasContent = !!node.content;
  const isExpandable = hasChildren || hasContent;

  return (
    <div className={cn('select-none', node.className)}>
      <div
        className={cn(
          'flex items-center py-2 px-3 rounded-md transition-colors duration-200 group cursor-pointer',
          isExpanded ? 'bg-accent/50' : 'hover:bg-accent/30',
          level === 0 && 'font-medium'
        )}
        onClick={() => isExpandable && setIsExpanded(!isExpanded)}
        style={{ paddingLeft: `${level * 1.5 + 0.75}rem` }}
      >
        <div className="flex items-center gap-2 flex-1 min-w-0">
          {isExpandable ? (
            <div className="text-muted-foreground/70 group-hover:text-foreground transition-colors flex-shrink-0">
              {isExpanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </div>
          ) : (
            <div className="w-4 flex-shrink-0" />
          )}

          {node.icon && <div className="text-primary/70 flex-shrink-0">{node.icon}</div>}

          <div className="flex-1 min-w-0 text-sm md:text-base truncate">
            {node.label}
          </div>

          {node.badge && <div className="ml-auto flex-shrink-0">{node.badge}</div>}
        </div>
      </div>

      <AnimatePresence>
        {isExpanded && isExpandable && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: 'easeInOut' }}
            className="overflow-hidden"
          >
            {hasChildren && (
              <div className="mt-1">
                {node.children!.map((child) => (
                  <TreeNode
                    key={child.id}
                    node={child}
                    defaultExpanded={defaultExpanded}
                    level={level + 1}
                  />
                ))}
              </div>
            )}
            {hasContent && (
              <div
                className="py-3 px-4 text-sm text-muted-foreground bg-muted/20 rounded-b-md border-l-2 border-primary/20 ml-6 mr-3 my-1"
                style={{ marginLeft: `${(level + 1) * 1.5}rem` }}
              >
                {node.content}
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
