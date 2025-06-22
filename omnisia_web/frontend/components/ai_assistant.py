"""
Assistente IA para OmnisIA Trainer Web
AI Assistant for OmnisIA Trainer Web

Assistente inteligente para auxiliar usuários em todas as tarefas
Intelligent assistant to help users with all tasks
"""

import streamlit as st
import asyncio
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger("omnisia.ai_assistant")


class AIAssistant:
    """
    Assistente IA integrado para auxiliar usuários
    Integrated AI assistant to help users
    """

    def __init__(self):
        self.conversation_history = []

        # Contexto do assistente
        self.system_prompt = """
        Você é o assistente IA do OmnisIA Trainer Web, uma plataforma avançada de treinamento de IA.
        
        Suas responsabilidades incluem:
        - Ajudar usuários com upload e processamento de arquivos
        - Orientar sobre treinamento de modelos (LoRA, fine-tuning)
        - Explicar configurações e parâmetros
        - Sugerir melhores práticas
        - Resolver problemas técnicos
        - Fornecer análises de performance
        
        Seja sempre útil, preciso e amigável. Responda em português por padrão.
        """

        self.quick_actions = [
            {
                "title": "📁 Como fazer upload?",
                "description": "Aprenda a fazer upload de arquivos",
                "prompt": "Como posso fazer upload de arquivos para a plataforma?",
            },
            {
                "title": "🧠 Configurar treinamento",
                "description": "Configure parâmetros de treinamento",
                "prompt": "Como configurar os parâmetros de treinamento LoRA?",
            },
            {
                "title": "📊 Analisar performance",
                "description": "Entenda métricas de performance",
                "prompt": "Como interpretar as métricas de performance do modelo?",
            },
            {
                "title": "🔧 Resolver problemas",
                "description": "Solucione problemas comuns",
                "prompt": "Meu treinamento está falhando. O que pode estar errado?",
            },
            {
                "title": "💡 Melhores práticas",
                "description": "Dicas para otimizar resultados",
                "prompt": "Quais são as melhores práticas para treinamento de modelos?",
            },
            {
                "title": "🌐 APIs externas",
                "description": "Configure APIs de modelos",
                "prompt": "Como configurar APIs externas como OpenAI, DeepSeek?",
            },
        ]

    def render_modal(self):
        """Renderiza modal do assistente / Render assistant modal"""
        if st.session_state.get("show_ai_assistant", False):
            with st.container():
                st.markdown("### 🤖 Assistente IA")
                st.markdown("*AI Assistant*")

                # Botão para fechar
                col1, col2 = st.columns([6, 1])
                with col2:
                    if st.button("❌", help="Fechar assistente"):
                        st.session_state["show_ai_assistant"] = False
                        st.rerun()

                # Ações rápidas
                self._render_quick_actions()

                # Chat interface
                self._render_chat_interface()

    def _render_quick_actions(self):
        """Renderiza ações rápidas / Render quick actions"""
        st.markdown("#### ⚡ Ações Rápidas")
        st.markdown("*Quick Actions*")

        # Grid de ações
        cols = st.columns(3)

        for i, action in enumerate(self.quick_actions):
            with cols[i % 3]:
                if st.button(
                    action["title"], help=action["description"], key=f"quick_action_{i}"
                ):
                    # Adicionar pergunta ao chat
                    self._add_message("user", action["prompt"])
                    # Gerar resposta
                    self._generate_response(action["prompt"])

    def _render_chat_interface(self):
        """Renderiza interface de chat / Render chat interface"""
        st.markdown("#### 💬 Chat")

        # Histórico de conversa
        if "assistant_messages" not in st.session_state:
            st.session_state.assistant_messages = [
                {
                    "role": "assistant",
                    "content": "Olá! Sou seu assistente IA. Como posso ajudá-lo hoje?",
                    "timestamp": datetime.now(),
                }
            ]

        # Container para mensagens
        messages_container = st.container()

        with messages_container:
            for message in st.session_state.assistant_messages:
                self._render_message(message)

        # Input para nova mensagem
        user_input = st.chat_input("Digite sua pergunta...")

        if user_input:
            # Adicionar mensagem do usuário
            self._add_message("user", user_input)

            # Gerar resposta
            with st.spinner("Gerando resposta..."):
                self._generate_response(user_input)

            st.rerun()

    def _render_message(self, message: Dict[str, Any]):
        """Renderiza uma mensagem / Render a message"""
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", datetime.now())

        if role == "user":
            # Mensagem do usuário (direita)
            st.markdown(
                f"""
            <div style="text-align: right; margin-bottom: 1rem;">
                <div style="display: inline-block; background: #667eea; color: white; 
                           padding: 0.75rem; border-radius: 15px 15px 5px 15px; 
                           max-width: 70%; text-align: left;">
                    {content}
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">
                    {timestamp.strftime("%H:%M")}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        else:
            # Mensagem do assistente (esquerda)
            st.markdown(
                f"""
            <div style="text-align: left; margin-bottom: 1rem;">
                <div style="display: inline-block; background: #f1f3f4; color: #333; 
                           padding: 0.75rem; border-radius: 15px 15px 15px 5px; 
                           max-width: 70%; border-left: 3px solid #667eea;">
                    🤖 {content}
                </div>
                <div style="font-size: 0.8rem; color: #666; margin-top: 0.25rem;">
                    {timestamp.strftime("%H:%M")}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    def _add_message(self, role: str, content: str):
        """Adiciona mensagem ao histórico / Add message to history"""
        message = {"role": role, "content": content, "timestamp": datetime.now()}

        st.session_state.assistant_messages.append(message)

    def _generate_response(self, user_input: str):
        """Gera resposta do assistente / Generate assistant response"""
        try:
            # Preparar contexto da conversa
            messages = [{"role": "system", "content": self.system_prompt}]

            # Adicionar histórico recente (últimas 10 mensagens)
            recent_messages = st.session_state.assistant_messages[-10:]
            for msg in recent_messages:
                if msg["role"] in ["user", "assistant"]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

            # Adicionar nova mensagem do usuário
            messages.append({"role": "user", "content": user_input})

            # Gerar resposta (simulada - implementar com API real)
            response = self._get_ai_response(user_input)

            # Adicionar resposta ao histórico
            self._add_message("assistant", response)

        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            self._add_message(
                "assistant",
                "Desculpe, ocorreu um erro ao processar sua pergunta. "
                "Tente novamente em alguns instantes.",
            )

    def _get_ai_response(self, user_input: str) -> str:
        """Gera resposta IA baseada na entrada / Generate AI response based on input"""
        # Implementação simplificada - substituir por chamada real à API

        user_input_lower = user_input.lower()

        if "upload" in user_input_lower:
            return """
            Para fazer upload de arquivos:
            
            1. **Acesse a página de Upload** 📁
            2. **Arraste e solte** seus arquivos ou clique em "Escolher arquivos"
            3. **Formatos suportados**: PDF, TXT, imagens (JPG, PNG), áudio (MP3, WAV), vídeo (MP4, AVI)
            4. **Tamanho máximo**: 500MB por arquivo
            5. **Processamento automático**: OCR para PDFs/imagens, transcrição para áudio/vídeo
            
            **Dica**: Para melhores resultados com OCR, use imagens com boa qualidade e contraste.
            """

        elif "treinamento" in user_input_lower or "lora" in user_input_lower:
            return """
            Configuração de treinamento LoRA:
            
            **Parâmetros principais**:
            - **Rank (r)**: 16 (padrão) - controla complexidade
            - **Alpha**: 32 - fator de escala
            - **Dropout**: 0.1 - regularização
            - **Épocas**: 3-10 dependendo do dataset
            - **Batch size**: 4-8 para GPU limitada
            
            **Dicas importantes**:
            - Comece com valores padrão
            - Monitore loss e accuracy
            - Use early stopping se loss parar de diminuir
            - Faça backup dos checkpoints
            """

        elif "performance" in user_input_lower or "métrica" in user_input_lower:
            return """
            Interpretação de métricas de performance:
            
            **Loss (Perda)**:
            - Deve diminuir ao longo das épocas
            - Se aumentar, pode ser overfitting
            
            **Accuracy (Precisão)**:
            - Porcentagem de predições corretas
            - >80% é considerado bom
            
            **Learning Rate**:
            - Muito alto: loss oscila
            - Muito baixo: treinamento lento
            
            **Dicas de monitoramento**:
            - Acompanhe gráficos em tempo real
            - Compare train vs validation loss
            - Use early stopping se necessário
            """

        elif "problema" in user_input_lower or "erro" in user_input_lower:
            return """
            Problemas comuns e soluções:
            
            **Treinamento lento**:
            - Reduza batch size
            - Use mixed precision (FP16)
            - Verifique uso de GPU
            
            **Out of Memory**:
            - Diminua batch size
            - Use gradient checkpointing
            - Libere cache da GPU
            
            **Loss não diminui**:
            - Ajuste learning rate
            - Verifique qualidade dos dados
            - Considere mais épocas
            
            **Modelo não converge**:
            - Normalize dados de entrada
            - Ajuste arquitetura
            - Verifique labels
            """

        elif "api" in user_input_lower:
            return """
            Configuração de APIs externas:
            
            **OpenAI**:
            - Obtenha API key em platform.openai.com
            - Configure OPENAI_API_KEY no .env
            - Modelos: GPT-4, GPT-3.5-turbo
            
            **DeepSeek**:
            - Registre-se em platform.deepseek.com
            - Configure DEEPSEEK_API_KEY
            - Modelo recomendado: deepseek-chat
            
            **AWS Bedrock**:
            - Configure credenciais AWS
            - Ative modelos no console
            - Configure região apropriada
            
            **Teste de conexão**:
            - Use health check na interface
            - Verifique logs para erros
            - Monitore uso e custos
            """

        else:
            return """
            Posso ajudá-lo com:
            
            📁 **Upload e processamento** de arquivos
            🧠 **Configuração de treinamento** de modelos
            📊 **Análise de performance** e métricas
            🔧 **Resolução de problemas** técnicos
            💡 **Melhores práticas** de IA
            🌐 **Configuração de APIs** externas
            
            Seja mais específico sobre o que precisa e terei prazer em ajudar!
            """

    def render_floating_button(self):
        """Renderiza botão flutuante do assistente / Render floating assistant button"""
        st.markdown(
            """
        <style>
        .floating-assistant {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
        }
        
        .floating-assistant:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        }
        </style>
        
        <button class="floating-assistant" onclick="toggleAssistant()">
            🤖
        </button>
        
        <script>
        function toggleAssistant() {
            // Implementar toggle do assistente
            window.parent.postMessage({type: 'toggle_assistant'}, '*');
        }
        </script>
        """,
            unsafe_allow_html=True,
        )


def main():
    """Função principal para teste / Main function for testing"""
    assistant = AIAssistant()

    st.title("🤖 Assistente IA - Teste")

    # Botão para mostrar assistente
    if st.button("Mostrar Assistente"):
        st.session_state["show_ai_assistant"] = True

    # Renderizar assistente
    assistant.render_modal()


if __name__ == "__main__":
    main()
