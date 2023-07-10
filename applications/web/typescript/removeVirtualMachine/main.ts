import { HandlerToRemoveVM } from "./handler";

const handlerToRemoveVirtualMachine = new HandlerToRemoveVM('.container', '.close');
handlerToRemoveVirtualMachine.addEventListeners();