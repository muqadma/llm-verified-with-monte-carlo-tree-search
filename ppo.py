from peft import LoraConfig
from trl import AutoModelForCausalLMWithValueHead, PPOConfig, PPOTrainer
from model import base_model_name
import llm_config

config = PPOConfig(
    model_name=base_model_name,
    learning_rate=1.41e-5,
    log_with='wandb',
    mini_batch_size=1,
    batch_size=1,
    gradient_accumulation_steps=1,
    early_stopping=False,
    target_kl=6.0,
    kl_penalty="kl",
    seed=0,
    use_score_scaling=False,
    use_score_norm=False,
    score_clip=None,
)

peft_config = LoraConfig(
    lora_alpha=16,
    #lora_dropout=0.1,
    r=16,
    bias="none",
    task_type="CAUSAL_LM",
)

base_model, model, tokenizer = llm_config.load_model()
base_model.config.use_cache = False
# More info: https://github.com/huggingface/transformers/pull/24906
base_model.config.pretraining_tp = 1

model = AutoModelForCausalLMWithValueHead.from_pretrained(
    model,
    trust_remote_code=True,
    device_map="auto",
    peft_config=peft_config)

ppo_trainer = PPOTrainer(
    model=model,
    config=config,
    tokenizer=tokenizer,
)

model_generation_args = llm_config.get_model_generation_args(tokenizer)

def generate(prompt):
    model_input = tokenizer(prompt, return_tensors="pt").to("cuda")
    qs = [model_input["input_ids"].squeeze(0)]
    ts = ppo_trainer.generate(qs, batch_size=1, **model_generation_args)
    rs = [tokenizer.decode(t.squeeze(), skip_special_tokens=True) for t in ts]
    text = rs[0]
    return (text, (qs, ts))

def trainer_step(query_tensors, response_tensors, rewards):
    stats = ppo_trainer.step(query_tensors, response_tensors, rewards)
    ppo_trainer.log_stats(stats, {}, rewards)

def save(fn="my_ppo_model"):
    ppo_trainer.save_pretrained(fn)
