# Daily Reflection Deterministic Decision Tree & AI Agent

## Description
This project implements a deterministic decision tree and a Python-based AI agent for daily self-reflection.

The system ensures that every input leads to a clear and consistent output using structured condition-based logic, avoiding ambiguity.

---

## Decision Logic

IF priority_done = yes → priority = done  
ELSE IF blocker_external = yes → priority = external_miss  
ELSE → priority = self_miss  

IF anxious OR flat → emotion = negative  
ELSE IF energized → emotion = positive  
ELSE → emotion = neutral  

IF goal_action = yes:
    IF focus_minutes ≥ 30 → progress = deep  
    ELSE → progress = light  
ELSE → progress = none  

IF repeated_mistake = yes:
    IF rule_exists = yes → improvement = recommit_rule  
    ELSE → improvement = define_new_rule  
ELSE → improvement = none  

---

## Output Format

```json
{
  "priority_status": "done | external_miss | self_miss | incomplete",
  "emotion": "negative | neutral | positive | incomplete",
  "progress": "deep | light | none | incomplete",
  "improvement": "recommit_rule | define_new_rule | none | incomplete"
}
