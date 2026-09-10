"""Stage 1: visual attribute extraction accuracy (spec §3.4.1).

Predicts building_type / bouwjaar / num_floors from street-view images.
Four cities, 20% frozen hold-out + 5-fold dev CV. Backbones: DINOv2 frozen
probe, ResNet-50 fine-tune, InternVL3-2B zero-shot (vlm/).
"""
