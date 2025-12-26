import services.llm_manager as llm_manager

prompt ="""
质感光照，自然光线，质感十足，画面聚焦于黄河，河水满是浑浊，显得暗沉且带有一丝神秘。整幅画面中只有这条河流，别无他物。在那浑浊的河水之中，一个巨大的蛟龙在水下游动，其身影由于河水的浑浊而若隐若现，龙的身形在水流的波动下似有似无，3D超高清画质效果，16K超高清画质效果"""

#image_url= llm_manager.dashscope_text2image(prompt)
#print(image_url)

#task_id = llm_manager.dashscope_image2video(prompt,image_url)
#print(task_id)


video_url = llm_manager.dashscope_task_status("49521608-00dd-4946-8fb0-21a82536c6fe")
print(video_url)