FROM public.ecr.aws/lambda/python:3.9

RUN yum install git -y \
 && yum clean all -y && rm -rf /var/cache/yum

RUN export AWS_PROFILE="default"

ENV NUMBA_CACHE_DIR='/tmp'

ARG FUNCTION_DIR="/var/task/"

WORKDIR /var/task/

COPY ./ ${FUNCTION_DIR}
# RUN apt-get update && apt-get install -y libgomp1

RUN pip install --default-timeout=500 -r requirements.txt \
    && python -m pip install --force-reinstall soundfile==0.12.1

# Grab the zappa handler.py and put it in the working directory
# RUN ZAPPA_HANDLER_PATH=$( \
#     python -c "from zappa import handler; print (handler.__file__)" \
#     ) \
#     && echo $ZAPPA_HANDLER_PATH \
#     && cp $ZAPPA_HANDLER_PATH ${FUNCTION_DIR}
#
#
# CMD [ "handler.lambda_handler" ]

CMD ["app.handler"]