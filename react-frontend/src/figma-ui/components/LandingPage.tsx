import { useNavigate } from 'react-router-dom';
import { Button } from './ui/button';
import { Card, CardContent } from './ui/card';
import {
  Sparkles,
  Users,
  MessageSquare,
  Lightbulb,
  ArrowRight,
  Zap,
  BarChart3,
  Shield,
  Github,
  Play,
  ChevronRight,
} from 'lucide-react';
import { motion } from 'framer-motion';

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.5, ease: 'easeOut' },
  }),
};

const PIPELINE_STEPS = [
  {
    icon: Users,
    title: 'Generate Personas',
    description: 'AI creates diverse, realistic user profiles with unique goals, motivations, and pain points.',
    color: 'text-blue-600',
    bg: 'bg-blue-50',
  },
  {
    icon: Play,
    title: 'Simulate Experiences',
    description: 'Each persona interacts with your product in a step-by-step simulated walkthrough.',
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
  },
  {
    icon: MessageSquare,
    title: 'Conduct Interviews',
    description: 'Structured Q&A sessions uncover reactions, frustrations, and desires from each persona.',
    color: 'text-violet-600',
    bg: 'bg-violet-50',
  },
  {
    icon: Lightbulb,
    title: 'Extract Needs',
    description: 'Latent user needs are identified, categorized, and prioritized from interview data.',
    color: 'text-amber-600',
    bg: 'bg-amber-50',
  },
];

const FEATURES = [
  {
    icon: Zap,
    title: 'Fast Results',
    description: 'Get actionable insights in minutes instead of weeks of user interviews.',
  },
  {
    icon: BarChart3,
    title: 'Analytics Built In',
    description: 'Track token usage, latency, and cost per analysis with a built-in dashboard.',
  },
  {
    icon: Shield,
    title: 'Reproducible',
    description: 'Run consistency tests to measure how stable your results are across iterations.',
  },
];

const NEED_CATEGORIES = [
  'Functional',
  'Usability',
  'Performance',
  'Safety',
  'Emotional',
  'Social',
  'Accessibility',
];

export function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted/30">
      {/* Navbar */}
      <nav className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur-md">
        <div className="max-w-6xl mx-auto flex items-center justify-between px-6 h-14">
          <div className="flex items-center gap-2 font-bold text-lg">
            <Sparkles className="w-5 h-5 text-primary" />
            NeedGen
          </div>
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm" asChild>
              <a
                href="https://github.com/AashutoshAgrawal/product-requirements-simulator"
                target="_blank"
                rel="noopener noreferrer"
              >
                <Github className="w-4 h-4" />
              </a>
            </Button>
            <Button size="sm" onClick={() => navigate('/app')}>
              Launch App
              <ArrowRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="max-w-4xl mx-auto text-center px-6 pt-24 pb-20">
          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            custom={0}
            className="inline-flex items-center gap-2 rounded-full border px-4 py-1.5 text-sm text-muted-foreground mb-6"
          >
            <Sparkles className="w-3.5 h-3.5" />
            Powered by the Elicitron methodology
          </motion.div>

          <motion.h1
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            custom={1}
            className="text-5xl sm:text-6xl font-bold tracking-tight leading-[1.1] mb-6"
          >
            Turn AI Into Your
            <br />
            <span className="underline decoration-primary/30 underline-offset-4">
              User Research Team
            </span>
          </motion.h1>

          <motion.p
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            custom={2}
            className="text-lg text-muted-foreground max-w-2xl mx-auto mb-10"
          >
            NeedGen generates diverse user personas, simulates their product
            experiences, interviews them, and extracts the latent needs that
            real users struggle to articulate — all in minutes.
          </motion.p>

          <motion.div
            initial="hidden"
            animate="visible"
            variants={fadeUp}
            custom={3}
            className="flex items-center justify-center gap-4"
          >
            <Button size="lg" onClick={() => navigate('/app')} className="text-base px-8">
              Try NeedGen
              <ArrowRight className="w-5 h-5 ml-1" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              onClick={() => {
                document.getElementById('how-it-works')?.scrollIntoView({ behavior: 'smooth' });
              }}
              className="text-base px-8"
            >
              See How It Works
            </Button>
          </motion.div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold mb-3">How It Works</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">
              A four-stage AI pipeline that mirrors real user research — from
              persona creation to actionable requirements.
            </p>
          </div>

          <div className="grid md:grid-cols-4 gap-6">
            {PIPELINE_STEPS.map((step, i) => (
              <motion.div
                key={step.title}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true, margin: '-40px' }}
                variants={fadeUp}
                custom={i}
              >
                <Card className="relative h-full border-2 hover:border-primary/20 transition-colors">
                  <CardContent className="pt-6">
                    {/* Step number */}
                    <div className="absolute -top-3 -left-2 w-7 h-7 rounded-full bg-primary text-primary-foreground text-xs font-bold flex items-center justify-center">
                      {i + 1}
                    </div>

                    <div className={`inline-flex items-center justify-center w-11 h-11 rounded-lg ${step.bg} mb-4`}>
                      <step.icon className={`w-5 h-5 ${step.color}`} />
                    </div>

                    <h3 className="font-semibold mb-2">{step.title}</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed">
                      {step.description}
                    </p>

                    {i < PIPELINE_STEPS.length - 1 && (
                      <ChevronRight className="hidden md:block absolute -right-5 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground/40" />
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Sample Output */}
      <section className="py-20 px-6 bg-muted/30">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-14">
            <h2 className="text-3xl font-bold mb-3">What You Get</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">
              Structured, categorized, and prioritized user needs ready for your product backlog.
            </p>
          </div>

          {/* Category pills */}
          <div className="flex flex-wrap justify-center gap-2 mb-10">
            {NEED_CATEGORIES.map((cat) => (
              <span
                key={cat}
                className="rounded-full border px-4 py-1.5 text-sm font-medium bg-background"
              >
                {cat}
              </span>
            ))}
          </div>

          {/* Sample need cards */}
          <div className="grid md:grid-cols-2 gap-4 max-w-3xl mx-auto">
            {[
              {
                category: 'Usability',
                priority: 'High',
                need: 'Users need intuitive onboarding that lets them accomplish their first task within 60 seconds of signing up.',
                implication: 'Design a guided walkthrough with contextual tooltips for first-time users.',
              },
              {
                category: 'Emotional',
                priority: 'Medium',
                need: 'Users need to feel a sense of progress and accomplishment as they use the product over time.',
                implication: 'Introduce milestone celebrations and visible progress indicators.',
              },
            ].map((need, i) => (
              <motion.div
                key={i}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                custom={i}
              >
                <Card className="border-2">
                  <CardContent className="pt-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-xs font-medium rounded-full bg-primary/10 px-2.5 py-0.5">
                        {need.category}
                      </span>
                      <span className={`text-xs font-medium rounded-full px-2.5 py-0.5 ${
                        need.priority === 'High'
                          ? 'bg-red-50 text-red-700'
                          : 'bg-yellow-50 text-yellow-700'
                      }`}>
                        {need.priority}
                      </span>
                    </div>
                    <p className="text-sm font-medium mb-2">{need.need}</p>
                    <p className="text-xs text-muted-foreground">
                      <span className="font-medium">Design implication:</span>{' '}
                      {need.implication}
                    </p>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            {FEATURES.map((feature, i) => (
              <motion.div
                key={feature.title}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                variants={fadeUp}
                custom={i}
                className="text-center"
              >
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-muted mb-4">
                  <feature.icon className="w-6 h-6 text-primary" />
                </div>
                <h3 className="font-semibold mb-1">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">
            Ready to discover what your users really need?
          </h2>
          <p className="text-muted-foreground mb-8">
            Start your first analysis in under a minute. No signup required.
          </p>
          <Button size="lg" onClick={() => navigate('/app')} className="text-base px-10">
            Launch NeedGen
            <ArrowRight className="w-5 h-5 ml-1" />
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8 px-6">
        <div className="max-w-6xl mx-auto flex items-center justify-between text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4" />
            NeedGen
          </div>
          <p>Based on the Elicitron research methodology</p>
        </div>
      </footer>
    </div>
  );
}
