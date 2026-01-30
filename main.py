import json
import os
from chains import observer_chain, interviewer_chain, feedback_chain
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


def clean(text):
    return "".join(c if c.isalnum() else "_" for c in text).lower()


def run_interview():
    team_name = "Team Rubleva"
    history = [] 
    turns_for_log = []
    
    print("--- Настройка интервью ---")
    pos = input("Введите позицию (например, Backend Developer): ")
    grade = input("Введите грейд (Junior/Middle/Senior): ")
    exp = input("Введите опыт (например, 1 год на Django): ")

    context_msg = f"ИНФОРМАЦИЯ О КАНДИДАТЕ: Позиция: {pos}, Грейд: {grade}, Опыт: {exp}. Исходи из этого при подборе сложности вопросов."
    history.append(SystemMessage(content=context_msg))

    print(f"\n--- Интервью началось ({pos}) ---")
    print("Введите 'Стоп', чтобы завершить и получить фидбек.\n")

    while True:
        user_input = input("Вы: ")
        
        if ("стоп" == user_input.lower()) or ("стоп игра" in user_input.lower()):
            break

        thoughts = observer_chain.invoke({
            "history": history,
            "user_input": user_input
        })

        response = interviewer_chain.invoke({
            "instruction": thoughts.instructions,
            "history": history,
            "user_input": user_input
        })
        
        message = response.content

        turn_id = len(turns_for_log) + 1
        current_turn = {
            "turn_id": turn_id,
            "agent_visible_message": message,
            "user_message": user_input,
            "internal_thoughts": f"[Observer]: {thoughts.analysis}. [Interviewer]: {thoughts.instructions}"
        }
        turns_for_log.append(current_turn)

        temp_log = {
            "team_name": team_name,
            "turns": turns_for_log
        }
        file_name_partial = f"log_{clean(pos)}_{clean(grade)}_{clean(exp)}_partial.json"
        with open(file_name_partial, "w", encoding="utf-8") as f:
            json.dump(temp_log, f, ensure_ascii=False, indent=2)

        history.append(HumanMessage(content=user_input))
        history.append(AIMessage(content=message))

        print(f"\nAI: {message}\n")

    print("\nГенерация финального отчета...")

    full_history_text = ""
    for t in turns_for_log:
        full_history_text += f"Мысли системы: {t['internal_thoughts']}\n"
        full_history_text += f"Кандидат: {t['user_message']}\n"
        full_history_text += f"Интервьюер: {t['agent_visible_message']}\n\n"
    final_report = feedback_chain.invoke({"log_history": full_history_text})

    final_log = {
        "team_name": team_name,
        "turns": turns_for_log,
        "final_feedback": final_report.model_dump()
    }
    file_name = f"log_{clean(pos)}_{clean(grade)}_{clean(exp)}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(final_log, f, ensure_ascii=False, indent=2)

    print("\n--- ИНТЕРВЬЮ ЗАВЕРШЕНО ---")
    print(f"Результат: {final_report.recommendation} ({final_report.grade})")
    print("Файл interview_log.json успешно сохранен.")

if __name__ == "__main__":
    run_interview()