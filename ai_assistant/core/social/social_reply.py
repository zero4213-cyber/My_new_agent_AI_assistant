import random

def reply_to_social_interaction(text):
    """
    Phản hồi tương tác xã hội bằng cách diễn đạt tự nhiên hơn,
    bắt chước cách giao tiếp thân thiện và đồng cảm.
    """
    text = text.lower()

    greetings = ["chào", "hi", "hello", "xin chào"]
    thanks = ["cảm ơn", "thank you", "thanks"]
    goodbyes = ["tạm biệt", "bye", "hẹn gặp lại"]
    sadness = ["buồn", "chán", "mệt", "khó khăn"]
    joy = ["vui", "hạnh phúc", "tuyệt", "thành công"]

    if any(word in text for word in greetings):
        return random.choice([
            "Chào bạn! Mình ở đây để giúp bạn bất cứ lúc nào. 😊",
            "Xin chào! Bạn cần hỗ trợ gì hôm nay?",
            "Rất vui được gặp bạn! 🤝"
        ])

    elif any(word in text for word in thanks):
        return random.choice([
            "Không có gì đâu, mình luôn sẵn sàng giúp đỡ bạn! 🙌",
            "Rất vui khi có thể hỗ trợ bạn!",
            "Cảm ơn bạn đã tin tưởng mình. ❤️"
        ])

    elif any(word in text for word in goodbyes):
        return random.choice([
            "Tạm biệt nhé! Chúc bạn một ngày tuyệt vời. 👋",
            "Hẹn gặp lại sớm!",
            "Chúc mọi điều tốt lành sẽ đến với bạn!"
        ])

    elif any(word in text for word in sadness):
        return random.choice([
            "Nếu bạn cảm thấy mệt mỏi, hãy nghỉ ngơi một chút nhé. Mọi chuyện rồi sẽ ổn. 🌧️➡️☀️",
            "Mình ở đây nếu bạn cần chia sẻ. Bạn không cô đơn đâu. 🤗",
            "Dù khó khăn đến đâu, bạn vẫn đang cố gắng — và điều đó rất tuyệt vời rồi."
        ])

    elif any(word in text for word in joy):
        return random.choice([
            "Thật tuyệt khi nghe bạn đang vui! 🎉",
            "Niềm vui của bạn cũng khiến mình thấy hạnh phúc lây đó!",
            "Hãy giữ tinh thần tích cực này mãi nhé! 🌟"
        ])

    return random.choice([
        "Cảm ơn vì đã chia sẻ! Nếu cần mình giúp điều gì, cứ nói nhé.",
        "Mình luôn sẵn sàng lắng nghe bạn.",
        "Bạn ổn chứ? Nếu có điều gì cần tâm sự, mình luôn ở đây."
    ])
