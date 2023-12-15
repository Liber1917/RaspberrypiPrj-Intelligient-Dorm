#include "stm32f10x.h"                  // Device header

void USART1_IRQHandler(void);
void LED(void);
void usart(void);
void delay_ms(u16 nms);
void PWM_TIM_init(uint16_t arr,uint16_t psc);
uint8_t 	Serial_RXData;

int main(void)
{   
    int i=0;
    usart();
    NVIC_PriorityGroupConfig(NVIC_PriorityGroup_2);
    PWM_TIM_init(199,7199);
    while(1)
    {
        if(Serial_RXData=='1')
        {
					for(i=0;i<=100;i++)
					{
          TIM_SetCompare1(TIM2,195);
          TIM_SetCompare2(TIM2,195);
					}
        }
        else if(Serial_RXData=='2') // Changed to 'else if' and added braces
        {
					for(i=0;i<=100;i++)
					{
          TIM_SetCompare1(TIM2,175);
          TIM_SetCompare2(TIM2,175);
					}
				}
		}
}

void usart (void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
  USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1|RCC_APB2Periph_GPIOA,ENABLE);
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_9; //IO口第9脚
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz; //IO口速度
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP; //IO口复用推挽输出
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_10; //IO口第10脚
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IPU; //IO口上拉输入
	GPIO_Init(GPIOA, &GPIO_InitStructure);
	
	USART_InitStructure.USART_BaudRate =9600;
	USART_InitStructure.USART_WordLength =USART_WordLength_8b;
	USART_InitStructure.USART_StopBits=USART_StopBits_1;
	USART_InitStructure.USART_Parity=USART_Parity_No;
	USART_InitStructure.USART_HardwareFlowControl=USART_HardwareFlowControl_None;
	USART_InitStructure.USART_Mode=USART_Mode_Rx;
	
	USART_Init(USART1,&USART_InitStructure);
	USART_Cmd(USART1, ENABLE); 
	
	NVIC_InitStructure.NVIC_IRQChannel=USART1_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority=1;
	NVIC_InitStructure.NVIC_IRQChannelSubPriority=1;
	NVIC_InitStructure.NVIC_IRQChannelCmd=ENABLE;
	
	NVIC_Init(&NVIC_InitStructure);
	
	USART_ITConfig(USART1,USART_IT_RXNE,ENABLE);
	
}


void USART1_IRQHandler (void)
{
	if(USART_GetITStatus(USART1,USART_IT_RXNE)==SET)
	{
		Serial_RXData=USART_ReceiveData(USART1);
		USART_ClearITPendingBit(USART1,USART_IT_RXNE);
	}
}

void LED(void)
{
	GPIO_InitTypeDef GPIO_InitStructure;

	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOC,ENABLE);
	
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_Out_PP;
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_13;
	GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOC,&GPIO_InitStructure);

}
void delay_ms(u16 nms)
{
	u32 temp;
	unsigned int fac_us=SystemCoreClock/8000000;
	unsigned int fac_ms=(u16)fac_us*1000;
	SysTick_CLKSourceConfig(SysTick_CLKSource_HCLK_Div8);
	SysTick->LOAD=(u32)nms*fac_ms;
	SysTick->VAL=0x00;
	SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk;
	do
		{
			temp=SysTick->CTRL;
		}while((temp&0x01)&&!(temp&(1<<16)));
		SysTick->CTRL&=~SysTick_CTRL_ENABLE_Msk;
		SysTick->VAL=0x00;
}
void PWM_TIM_init(uint16_t arr,uint16_t psc)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	TIM_TimeBaseInitTypeDef TIM_TimeBasestructure;
	TIM_OCInitTypeDef TIM_OCInitStructure;
	
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA,ENABLE);
	
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM2,ENABLE);
	
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_0;
	GPIO_InitStructure.GPIO_Mode=GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Speed=GPIO_Speed_50MHz;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
	
	GPIO_InitStructure.GPIO_Pin=GPIO_Pin_1;
	GPIO_Init(GPIOA,&GPIO_InitStructure);
	
	TIM_TimeBasestructure.TIM_Period=arr;
	TIM_TimeBasestructure.TIM_Prescaler=psc;
	TIM_TimeBasestructure.TIM_ClockDivision=TIM_CKD_DIV1;
	TIM_TimeBasestructure.TIM_CounterMode=TIM_CounterMode_Up ;
	TIM_TimeBaseInit(TIM2,&TIM_TimeBasestructure);
	
	TIM_OCStructInit(&TIM_OCInitStructure);
	TIM_OCInitStructure.TIM_OCMode=TIM_OCMode_PWM2   ;
	TIM_OCInitStructure.TIM_OutputState=TIM_OutputState_Enable ;
	TIM_OCInitStructure.TIM_Pulse = 0;
	TIM_OCInitStructure.TIM_OCPolarity =TIM_OCPolarity_High;
	TIM_OC1Init(TIM2,&TIM_OCInitStructure);
	TIM_OC2Init(TIM2,&TIM_OCInitStructure);
	TIM_OC3Init(TIM2,&TIM_OCInitStructure);
	TIM_OC4Init(TIM2,&TIM_OCInitStructure);
	
	TIM_CtrlPWMOutputs(TIM2,ENABLE);
	
	TIM_OC1PreloadConfig(TIM2,TIM_OCPreload_Enable);
	TIM_OC2PreloadConfig(TIM2,TIM_OCPreload_Enable);
	TIM_OC3PreloadConfig(TIM2,TIM_OCPreload_Enable);
	TIM_OC4PreloadConfig(TIM2,TIM_OCPreload_Enable);
	
	TIM_ARRPreloadConfig(TIM2, ENABLE);
	
	TIM_Cmd(TIM2,ENABLE);
}
	
	


