from pathlib import Path
from buster.mind.cognitive_loop import CognitiveLoopEngine
from buster.mind.internal_dialogue import InternalDialogue
from buster.mind.dream_mode import DreamMode
from buster.mind.self_improvement import SelfImprovementEngine
from buster.mind.continuous_runtime import ContinuousMindRuntime
from buster.perception.cognitive_loop_bridge import perception_to_cognitive_observations
from buster.brain.planner.cognitive_loop_planner_bridge import cognitive_loop_context_for_planner
from buster.workspace.cognitive_loop_dashboard import CognitiveLoopDashboard

def main():
    loop=CognitiveLoopEngine()
    result=loop.tick([{'source':'test','type':'wake_word','summary':'Buster heard his name','priority':9,'confidence':0.95}])
    assert result['state']['tick_count'] >= 1
    assert result['thoughts']
    dialogue=InternalDialogue(); msg=dialogue.say('Planner','I am reviewing the goal loop.',target='Builder',confidence=0.9)
    assert msg['agent']=='Planner' and dialogue.recent(1)[0]['target']=='Builder'
    dream=DreamMode(); reflection=dream.reflect({'patterns':[{'name':'tkinter_layout'}]*3,'goals':[{'title':'Improve UI'}]})
    assert reflection['recommendations']
    improver=SelfImprovementEngine(); proposals=improver.analyze_patterns([{'name':'import_fix'},{'name':'import_fix'},{'name':'import_fix'}])
    assert proposals and proposals[0]['requires_user_approval'] is True
    observations=perception_to_cognitive_observations([{'source':'ears','type':'speech','summary':'User said Buster','priority':9,'confidence':0.92},{'source':'ambient','type':'fan','summary':'Fan noise','priority':2,'confidence':0.4}])
    assert len(observations)==1
    runtime=ContinuousMindRuntime(provider=lambda: observations, interval=0.01); once=runtime.tick_once(); assert 'state' in once
    planner_context=cognitive_loop_context_for_planner(loop.status()); assert 'cognitive_phase' in planner_context
    dash=CognitiveLoopDashboard().snapshot(); assert dash['title']=='Cognitive Loop'
    for path in ['data/cognitive_loop_state.json','data/internal_thoughts.json','data/internal_dialogue.json','data/dream_reflections.json','data/self_improvement_missions.json']:
        assert Path(path).exists(), path
    print('SUCCESS: v5.5 Cognitive Loop Engine tests passed')
if __name__=='__main__': main()
