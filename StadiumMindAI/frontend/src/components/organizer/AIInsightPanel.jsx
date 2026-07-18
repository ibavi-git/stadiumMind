import React from 'react';
import Card from '../ui/Card';
import Badge from '../ui/Badge';
import { Brain, MapPin, Clock, Zap } from 'lucide-react';

export default function AIInsightPanel({ insights = [], loading = false }) {
  return (
    <Card className="h-full flex flex-col">
      <div className="flex items-center justify-between mb-4 border-b border-white/10 pb-4">
        <div className="flex items-center gap-2">
          <div className="bg-purple-500/20 p-2 rounded-lg">
            <Brain className="h-5 w-5 text-purple-400" />
          </div>
          <h2 className="font-bold text-lg">AI Insights</h2>
        </div>
        <span className="text-[10px] uppercase tracking-wider font-semibold text-purple-300 bg-purple-500/20 px-2 py-1 rounded">
          Powered by Gemini
        </span>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 space-y-4 scrollbar-hide">
        {loading ? (
          [1, 2, 3].map(i => (
            <div key={i} className="animate-pulse bg-white/5 rounded-lg p-4 h-32"></div>
          ))
        ) : insights.length === 0 ? (
          <div className="text-center py-8 text-gray-400">
            <Zap className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p>No active insights at the moment.</p>
          </div>
        ) : (
          insights.map((insight, idx) => (
            <div 
              key={idx} 
              className={`bg-white/5 rounded-lg p-4 border-l-2 animate-fade-in ${
                insight.priority === 'HIGH' ? 'border-l-red-500' :
                insight.priority === 'MEDIUM' ? 'border-l-orange-500' :
                'border-l-blue-500'
              }`}
              style={{ animationDelay: `${idx * 100}ms` }}
            >
              <div className="flex justify-between items-start mb-2">
                <Badge status={insight.priority === 'HIGH' ? 'CRITICAL' : insight.priority === 'MEDIUM' ? 'HIGH' : 'ACTIVE'} />
                {insight.time_sensitive && (
                  <Clock className="h-4 w-4 text-red-400 animate-pulse" />
                )}
              </div>
              
              <div className="flex items-center text-sm font-medium text-gray-300 mb-2">
                <MapPin className="h-3 w-3 mr-1" />
                {insight.zone}
              </div>
              
              <p className="text-sm mb-3 text-gray-100">{insight.insight}</p>
              
              <div className="bg-black/30 rounded p-2 text-xs">
                <span className="font-bold text-blue-300">Action: </span>
                <span className="text-gray-300">{insight.action}</span>
              </div>
            </div>
          ))
        )}
      </div>
    </Card>
  );
}
