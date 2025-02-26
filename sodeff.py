import streamlit as st
from pydub import AudioSegment
import numpy as np
import io

# عنوان التطبيق
st.title("Cinematic Sound Effects")

# تحميل الملف الصوتي
uploaded_file = st.file_uploader("Upload an audio file (MP3 or WAV)", type=["mp3", "wav"])

def apply_echo(audio, delay, decay):
    """
    تطبيق تأثير الصدى على الصوت.
    :param audio: الملف الصوتي (AudioSegment).
    :param delay: التأخير بين الصدى والأصلي (بالمللي ثانية).
    :param decay: قوة الصدى (نسبة من 0 إلى 1).
    :return: الصوت مع تأثير الصدى.
    """
    # تحويل الصوت إلى numpy array
    samples = np.array(audio.get_array_of_samples())
    sample_rate = audio.frame_rate

    # حساب عدد العينات للتأخير
    delay_samples = int(delay * sample_rate / 1000)

    # إنشاء نسخة من الصوت مع الصدى
    echoed_samples = np.zeros(len(samples) + delay_samples)
    echoed_samples[:len(samples)] += samples
    echoed_samples[delay_samples:] += samples[:-delay_samples] * decay

    # تحويل النتيجة إلى AudioSegment
    echoed_audio = audio._spawn(echoed_samples.astype(np.int16))
    return echoed_audio

if uploaded_file is not None:
    # قراءة الملف الصوتي
    audio = AudioSegment.from_file(uploaded_file)

    # عرض خيارات المؤثرات
    st.write("Choose the effects to apply:")
    pitch_shift_amount = st.slider("Pitch Shift", -12, 12, 0, help="Adjust the pitch of the audio.")
    echo_delay = st.slider("Echo Delay (ms)", 0, 1000, 200, help="Delay between echoes in milliseconds.")
    echo_decay = st.slider("Echo Decay", 0.0, 1.0, 0.5, help="Decay factor for the echo effect.")

    # تطبيق تغيير طبقة الصوت (Pitch Shift)
    if pitch_shift_amount != 0:
        # تغيير السرعة لتغيير طبقة الصوت
        new_sample_rate = int(audio.frame_rate * (2.0 ** (pitch_shift_amount / 12.0)))
        audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
        audio = audio.set_frame_rate(44100)  # إعادة ضبط معدل الإطار إلى القيمة الافتراضية

    # تطبيق الصدى (Echo)
    if echo_delay > 0:
        audio = apply_echo(audio, echo_delay, echo_decay)

    # تشغيل الصوت المعدل
    st.audio(audio.export(format="wav").read(), format="audio/wav")

    # تنزيل الملف المعدل
    st.download_button(
        label="Download Modified Audio",
        data=audio.export(format="wav").read(),
        file_name="modified_audio.wav",
        mime="audio/wav"
    )
else:
    st.write("Please upload an audio file to start editing.")




    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            .stDeployButton {display:none;}
            #stStreamlitLogo {display: none;}
            a {
                text-decoration: none;
                color: inherit;
                pointer-events: none;
            }
            a:hover {
                text-decoration: none;
                color: inherit;
                cursor: default;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)