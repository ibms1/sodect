import streamlit as st
from pydub import AudioSegment
import numpy as np
import io

# عنوان التطبيق
st.title("Cinematic Sound Effects")

# تحميل الملف الصوتي
uploaded_file = st.file_uploader("Upload an audio file (MP3 or WAV)", type=["mp3", "wav"])

def apply_echo_alternative(audio, delay, decay):
    """
    تطبيق تأثير الصدى على الصوت باستخدام طريقة بديلة.
    :param audio: الملف الصوتي (AudioSegment).
    :param delay: التأخير بين الصدى والأصلي (بالمللي ثانية).
    :param decay: قوة الصدى (نسبة من 0 إلى 1).
    :return: الصوت مع تأثير الصدى.
    """
    # If no echo, return the original
    if delay == 0 or decay == 0:
        return audio
    
    # Create the echo effect by overlaying the original with a delayed version
    delayed_audio = audio - (10 * (1 - decay))  # Reduce volume by decay factor (in dB)
    
    # Create silence for the delay
    silence = AudioSegment.silent(duration=delay)
    
    # Add silence at the beginning of the delayed audio
    delayed_audio = silence + delayed_audio
    
    # Overlay the original with the delayed version
    combined = audio.overlay(delayed_audio, position=0)
    
    return combined

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
    # تطبيق الصدى (Echo)
if echo_delay > 0 and echo_decay > 0:
    try:
        # First try the primary function
        # audio = apply_echo(audio, echo_delay, echo_decay)
        raise NotImplementedError("apply_echo function is not implemented.")
    except Exception as e:
        st.warning(f"Using alternative echo method.")
        # Fall back to the alternative if there's an error
        audio = apply_echo_alternative(audio, echo_delay, echo_decay)

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